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
