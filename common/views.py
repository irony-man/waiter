import json
import uuid

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer  # type: ignore
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Case, F, Prefetch, Q, Sum, When
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from loguru import logger
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from common.forms import LoginForm
from common.model_helpers import generate_chain_name, generate_username
from common.models import (
    Category,
    Chain,
    MenuItem,
    Order,
    OrderItem,
    Restaurant,
    Table,
    UserProfile,
)
from common.serializers import (
    CategorySerializer,
    LiteCategorySerializer,
    LiteMenuItemSerializer,
    LiteUserProfileSerializer,
    MenuItemSerializer,
    OrderSerializer,
    RestaurantSerializer,
    TableSerializer,
    UserProfileSerializer,
)
from common.tasks import import_menu_items
from common.taxonomies import OrderStatus, PriceType


def is_ajax(request) -> bool:
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def is_valid_uid(uid, version=4) -> bool:
    try:
        uuid.UUID(uid, version=version)
    except ValueError:
        return False
    return True


class AuthMixin:
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AuthMixin, self).dispatch(  # noqa
            request, *args, **kwargs
        )


class HomePage(TemplateView):
    template_name = "common/home.html"


class DashboardPage(AuthMixin, TemplateView):
    template_name = "common/home.html"


class LoginView(FormView):
    form_class = LoginForm
    template_name = "common/login.html"
    success_url = reverse_lazy("common:dashboard")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form: LoginForm):
        logger.info(form.cleaned_data)
        if form.cleaned_data.get("is_guest"):
            user = User.objects.create(username=generate_username())
            chain, _ = Chain.objects.get_or_create(name=generate_chain_name())
            UserProfile.objects.create(user=user, chain=chain, is_guest=True)
        else:
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(
                self.request, username=username, password=password
            )
            if not user:
                form.errors.password = ("Invalid login credentials!!",)
                return super(LoginView, self).form_invalid(form)
        login(self.request, user)
        return redirect(self.success_url)

    def form_invalid(self, form):
        if is_ajax(self.request):
            return JsonResponse(
                {"status": 400, "errors": form.errors}, status=400
            )
        return super(LoginView, self).form_invalid(form)


class Logout(AuthMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse("common:home"))


class UserProfileViewSet(AuthMixin, ModelViewSet):
    lookup_field = "uid"
    serializer_class = LiteUserProfileSerializer
    http_method_names = ("get", "patch")

    def get_queryset(self):
        return UserProfile.objects.all()


class UserViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    http_method_names = ("get", "patch")

    def get_queryset(self):
        if self.request.method.upper() == "PATCH" and self.kwargs.get("uid"):
            return UserProfile.objects.filter(user=self.request.user)
        return UserProfile.objects.all()

    def get_object(self):
        if self.request.user.is_authenticated:
            return UserProfile.objects.get(user=self.request.user)
        uid = self.request.session.get("uid", str(uuid.uuid4()))
        self.request.session["uid"] = uid
        return UserProfile(uid=uid)


class RestaurantViewSet(AuthMixin, ModelViewSet):
    lookup_field = "uid"
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.filter(chain=self.request.chain)

    def perform_create(self, serializer):
        return serializer.save(chain=self.request.chain)

    def destroy(self, request, **kwargs):
        instance = self.get_object()
        for category in instance.category_set.all():
            category.menuitem_set.all().delete()
            category.delete()
        instance.table_set.all().delete()
        return super(RestaurantViewSet, self).destroy(request, **kwargs)

    @action(methods=["POST"], detail=True)
    def import_menu(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.category_set.count():
                raise ValueError("This restaurant already has categories!!")
            import_menu_items(instance.id)
            return Response(status=HTTP_200_OK)
        except Exception as e:
            raise ValidationError(dict(detail=e))

    @action(methods=["DELETE"], detail=True)
    def table(self, request, *args, **kwargs):
        instance = self.get_object()
        table_last = instance.table_set.last()
        if not table_last:
            return Response(status=HTTP_404_NOT_FOUND)
        table_last.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class TableViewSet(ModelViewSet):
    lookup_field = "uid"
    serializer_class = TableSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("restaurant__uid",)
    http_method_names = ("get", "post", "delete")

    def get_queryset(self):
        if self.request.method.upper() == "GET":
            return Table.objects.all()
        return Table.objects.filter(
            restaurant__chain=self.request.chain
        ).order_by("number")

    @action(methods=["GET"], detail=True)
    def categories(self, request, *args, **kwargs):
        try:
            instance: Table = self.get_object()
            data = dict(
                table=TableSerializer(instance=instance).data, categories=[]
            )
            search_term = request.GET.get("search", "")
            categories = instance.restaurant.category_set.order_by(
                "name"
            ).prefetch_related(
                Prefetch(
                    "menuitem_set",
                    queryset=MenuItem.objects.filter(
                        Q(name__icontains=search_term)
                        | Q(description__icontains=search_term)
                    ),
                    to_attr="filtered_menuitems",
                )
            )

            for category in categories:
                menu_items = category.filtered_menuitems
                if not len(menu_items):
                    continue
                total_half_price = sum(item.half_price for item in menu_items)
                data["categories"].append(
                    {
                        "category": LiteCategorySerializer(
                            instance=category
                        ).data,
                        "has_half_price": total_half_price > 0,
                        "menu_items_count": len(menu_items),
                        "menu_items": LiteMenuItemSerializer(
                            instance=menu_items, many=True
                        ).data,
                    }
                )

            return Response(data=data, status=HTTP_200_OK)
        except Http404:
            raise Http404
        except Exception as e:
            raise ValidationError(dict(detail=e))

    @action(methods=["GET"], detail=True)
    def cart(self, request, *args, **kwargs):
        try:
            instance: Table = self.get_object()
            data = dict(table=TableSerializer(instance=instance).data, cart={})
            cart = json.loads(request.COOKIES.get("cart", "{}"))
            for key, val in cart.items():
                uid, price_type = key.split("/", 1)
                if (
                    menu_item := MenuItem.objects.filter(
                        uid=uid,
                        available=True,
                        category__restaurant=instance.restaurant,
                    ).first()
                ) and (quantity := val.get("quantity", 0)):
                    data["cart"][key] = dict(
                        menu_item=LiteMenuItemSerializer(
                            instance=menu_item
                        ).data,
                        price=menu_item.half_price
                        if price_type == PriceType.HALF
                        else menu_item.full_price,
                        price_type=price_type,
                        quantity=quantity,
                    )
            return Response(data=data, status=HTTP_200_OK)
        except Http404:
            raise Http404
        except Exception as e:
            raise ValidationError(dict(detail=e))


class CategoryViewSet(AuthMixin, ModelViewSet):
    lookup_field = "uid"
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("restaurant__uid",)
    search_fields = ("name",)

    def get_queryset(self):
        return Category.objects.filter(
            restaurant__chain=self.request.chain
        ).order_by("name")


class MenuItemViewSet(AuthMixin, ModelViewSet):
    lookup_field = "uid"
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("category__uid",)
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        if self.request.method.upper() == "GET":
            return MenuItem.objects.all()
        return MenuItem.objects.filter(
            category__restaurant__chain=self.request.chain
        )


class OrderViewSet(AuthMixin, ModelViewSet):
    lookup_field = "uid"
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("table__restaurant__uid", "status")
    ordering_fields = ("created",)
    http_method_names = ("get",)

    def get_queryset(self):
        return Order.objects.filter(
            table__restaurant__chain=self.request.chain
        )


class OrderAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            uid = kwargs.get("uid", None)
            if not uid or not is_valid_uid(uid):
                raise Http404
            request.session["uid"] = request.session.get(
                "uid", str(uuid.uuid4())
            )
            instance = Table.objects.get(uid=uid)
            orders = Order.objects.filter(
                table=instance, session_uid=request.session["uid"]
            )
            data = dict(
                table=TableSerializer(instance=instance).data,
                orders=OrderSerializer(instance=orders, many=True).data,
                session_uid=request.session["uid"],
                total_price=sum(o.total_price for o in orders),
            )
            return Response(data=data, status=HTTP_200_OK)
        except Http404:
            raise Http404
        except Exception as e:
            raise ValidationError(dict(detail=e))

    def post(self, request, *args, **kwargs):
        try:
            uid = kwargs.get("uid", None)
            if not uid or not is_valid_uid(uid):
                raise Http404
            instance = Table.objects.get(uid=uid)
            request.session["uid"] = request.session.get(
                "uid", str(uuid.uuid4())
            )
            request.session["table"] = str(instance.uid)
            cart = json.loads(request.COOKIES.get("cart", "{}"))
            order, _ = Order.objects.get_or_create(
                table=instance,
                status=OrderStatus.PENDING,
                session_uid=request.session["uid"],
            )
            for key, val in cart.items():
                menu_uid, price_type = key.split("/", 1)
                menu_item = MenuItem.objects.filter(
                    uid=menu_uid, available=True
                ).first()

                if not menu_item:
                    continue

                quantity = val.get("quantity", 0)
                item, created = OrderItem.objects.get_or_create(
                    order=order,
                    menu_item=menu_item,
                    price_type=price_type,
                    defaults={"quantity": quantity},
                )

                if not created:
                    item.quantity += quantity

                item.clean()
                item.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                str(order.session_uid),
                {
                    "type": "send_order",
                    "order": order,
                },
            )
            async_to_sync(channel_layer.group_send)(
                str(order.table.restaurant.uid),
                {
                    "type": "send_order",
                    "order": order,
                },
            )
            return Response(status=HTTP_200_OK)
        except Http404:
            raise Http404
        except Exception as e:
            raise ValidationError(dict(detail=e))
