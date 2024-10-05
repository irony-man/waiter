from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.generic import CreateView, DetailView, FormView, TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from loguru import logger
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from common.forms import LoginForm, LoginPinRequestForm
from common.model_helpers import now_time
from common.models import (
    Category,
    LoginPinRequest,
    MenuItem,
    Restaurant,
    Table,
    UserProfile,
)
from common.serializers import (
    CategorySerializer,
    LiteUserProfileSerializer,
    LoginSerializer,
    MenuItemSerializer,
    RestaurantSerializer,
    TableSerializer,
    UserProfileSerializer,
)


def is_ajax(request) -> bool:
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


class AuthMixin:
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AuthMixin, self).dispatch(  # noqa
            request, *args, **kwargs
        )


class HomePage(AuthMixin, TemplateView):
    template_name = "common/home.html"


class LoginPinRequestView(CreateView):
    form_class = LoginPinRequestForm
    template_name = "common/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("common:home")
        return super(LoginPinRequestView, self).dispatch(
            request, *args, **kwargs
        )

    def form_valid(self, form: LoginPinRequestForm):
        instance: LoginPinRequest = form.cleaned_data.get("instance")
        if not str(instance.user.userprofile.phone).startswith("322"):
            pass
            # send_otp_sms.apply_async(
            #     args=(instance.msg_body, str(instance.user.userprofile.phone))
            # )
        if is_ajax(self.request):
            return JsonResponse(
                {
                    "status": 200,
                    "otp_resend_time": instance.otp_resend_remaining_time,
                }
            )
        return redirect(
            reverse_lazy(
                "common:login-pin-verify", kwargs={"uid": instance.uid}
            )
        )

    def form_invalid(self, form):
        if is_ajax(self.request):
            return JsonResponse(
                {"status": 400, "errors": form.errors}, status=400
            )
        return super(LoginPinRequestView, self).form_invalid(form)


class LoginPinVerifyView(FormView):
    form_class = LoginForm
    template_name = "common/verify.html"
    success_url = reverse_lazy("common:home")

    @cached_property
    def pin_request(self):
        return get_object_or_404(LoginPinRequest, uid=self.kwargs.get("uid"))

    def get_form(self, form_class=None):
        if self.request.method.upper() == "POST":
            data = self.request.POST.copy()
            data["phone"] = self.pin_request.user.username
            return self.form_class(data)
        return self.form_class()

    def get_context_data(self, **kwargs):
        ctx = super(LoginPinVerifyView, self).get_context_data(**kwargs)
        ctx["pin_request"] = self.pin_request
        ctx[
            "otp_resend_remaining_time"
        ] = self.pin_request.otp_resend_remaining_time
        return ctx

    def form_valid(self, form: LoginForm):
        login(self.request, form.cleaned_data["user"])
        headers = {
            k: v
            for k, v in self.request.META.items()
            if k.startswith(("HTTP_", "SERVER_", "REMOTE_", "REQUEST_"))
        }
        pin_req = self.pin_request
        pin_req.used = True
        pin_req.used_timestamp = now_time()
        pin_req.save()
        # data = LiteUserSerializer(instance=self.request.user).data
        # send_to_jheel.apply_async(
        #   args=(JheelMessageType.USER, JheelSubMessageType.USER_LOGIN, data)
        # )
        return redirect(self.success_url)


class Logout(AuthMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse("common:home"))


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(request, username=username, password=password)
            if not user:
                return Response(
                    {"message": "Invalid login credentials!!"},
                    status=HTTP_400_BAD_REQUEST,
                )
            login(request, user)
            return Response(
                UserProfileSerializer(instance=user.userprofile).data,
                status=HTTP_200_OK,
            )

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class Logout(AuthMixin, APIView):
    def get(self, request, *args, **kwargs):
        try:
            logout(request)
            return Response({"message": "Successfully logged out!!"})
        except Exception as e:
            logger.error(e)
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileViewSet(AuthMixin, ModelViewSet):
    lookup_field = "uid"
    serializer_class = LiteUserProfileSerializer
    http_method_names = ("get", "patch")

    def get_queryset(self):
        return UserProfile.objects.all()


class UserViewSet(ModelViewSet):
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


class TableViewSet(AuthMixin, ModelViewSet):
    lookup_field = "uid"
    serializer_class = TableSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("restaurant__uid",)

    def get_queryset(self):
        return Table.objects.all().order_by("number")


class CategoryViewSet(AuthMixin, ModelViewSet):
    lookup_field = "uid"
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("restaurant__uid",)
    search_fields = ("name",)

    def get_queryset(self):
        return Category.objects.all().order_by("name")


class MenuItemViewSet(AuthMixin, ModelViewSet):
    lookup_field = "uid"
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("category__uid",)
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        return MenuItem.objects.all()
