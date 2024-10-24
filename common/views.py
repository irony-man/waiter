import json
import uuid

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Case, F, Sum, When
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from common.forms import LoginPinRequestForm
from common.models import (
    Category,
    MenuItem,
    Order,
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
from common.taxonomies import PriceType


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


class LoginPinRequestView(CreateView):
    form_class = LoginPinRequestForm
    template_name = "common/login.html"
    success_url = reverse_lazy("common:dashboard")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super(LoginPinRequestView, self).dispatch(
            request, *args, **kwargs
        )

    def form_valid(self, form: LoginPinRequestForm):
        login(self.request, form.cleaned_data.get("instance"))
        return redirect(self.success_url)

    def form_invalid(self, form):
        if is_ajax(self.request):
            return JsonResponse(
                {"status": 400, "errors": form.errors}, status=400
            )
        return super(LoginPinRequestView, self).form_invalid(form)


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


class UserViewSet(AuthMixin, ModelViewSet):
    serializer_class = UserProfileSerializer
    http_method_names = ("get", "post", "patch")

    def get_queryset(self):
        if self.request.method.upper() == "PATCH" and self.kwargs.get("uid"):
            return UserProfile.objects.filter(user=self.request.user)
        return UserProfile.objects.all()

    def get_object(self):
        if self.request.user.is_authenticated:
            return UserProfile.objects.get(user=self.request.user)


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
            for category in Category.objects.filter(
                restaurant=instance.restaurant
            ).order_by("name"):
                items = MenuItem.objects.filter(category=category)
                data["categories"].append(
                    dict(
                        category=LiteCategorySerializer(
                            instance=category,
                        ).data,
                        has_half_price=items.aggregate(
                            total_half_price=Sum("half_price", default=0)
                        ).get("total_half_price", 0)
                        > 0,
                        menu_items=LiteMenuItemSerializer(
                            instance=items,
                            many=True,
                        ).data,
                    )
                )
            return Response(data=data, status=HTTP_200_OK)
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
    http_method_names = ("get",)

    def get_queryset(self):
        return Order.objects.filter(
            session_uid=self.request.session.get("uid", None)
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
            total_price = orders.aggregate(
                total_price=Sum(
                    Case(
                        When(
                            price_type=PriceType.FULL,
                            then=F("menu_item__full_price") * F("quantity"),
                        ),
                        When(
                            price_type=PriceType.HALF,
                            then=F("menu_item__half_price") * F("quantity"),
                        ),
                    )
                )
            ).get("total_price", 0)
            data = dict(
                table=TableSerializer(instance=instance).data,
                orders=OrderSerializer(instance=orders, many=True).data,
                session_uid=request.session["uid"],
                total_price=total_price,
            )
            return Response(data=data, status=HTTP_200_OK)
        except Exception as e:
            raise ValidationError(dict(detail=e))

    def post(self, request, *args, **kwargs):
        try:
            uid = kwargs.get("uid", None)
            if not uid or not is_valid_uid(uid):
                raise Http404
            instance = Table.objects.get(uid=uid)
            request.session["table"] = str(instance.uid)
            request.session["uid"] = request.session.get(
                "uid", str(uuid.uuid4())
            )
            orders = []
            cart = json.loads(request.COOKIES.get("cart", "{}"))
            for key, val in cart.items():
                uid, price_type = key.split("/", 1)
                order_ser = OrderSerializer(
                    data=dict(
                        menu_item=uid,
                        table=instance.uid,
                        price_type=price_type,
                        quantity=val.get("quantity", 0),
                        session_uid=request.session["uid"],
                    )
                )
                if order_ser.is_valid():
                    orders.append(order_ser.save())
            return Response(status=HTTP_201_CREATED)
        except Exception as e:
            raise ValidationError(dict(detail=e))
