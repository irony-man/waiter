from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from common import views

router = DefaultRouter()

router.register("user", views.UserViewSet, basename="user")
router.register(
    "user-profile", views.UserProfileViewSet, basename="user-profile"
)
router.register("restaurant", views.RestaurantViewSet, basename="restaurant")
router.register("table", views.TableViewSet, basename="table")
router.register("category", views.CategoryViewSet, basename="category")
router.register("menu-item", views.MenuItemViewSet, basename="menu-item")

urlpatterns = [
    path("login/", views.LoginPinRequestView.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    re_path("^dashboard/", views.DashboardPage.as_view(), name="dashboard"),
    re_path("^", views.HomePage.as_view(), name="home"),
]
