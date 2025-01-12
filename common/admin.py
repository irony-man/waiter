# App Imports
from django.apps import apps
from django.contrib import admin

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


@admin.register(Chain)
class ChainAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "chain")
    search_fields = (
        "user__email",
        "user__username",
        "user__first_name",
        "user__last_name",
        "chain__name",
    )
    list_filter = ("chain",)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "chain")
    list_filter = ("chain",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant")
    search_fields = ("name", "restaurant__name")
    list_filter = ("restaurant",)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "restaurant")
    list_filter = ("restaurant", "restaurant__chain")
    readonly_fields = ("qr_code", "qr_code_response")


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "menu_type",
        "available",
        "half_price",
        "full_price",
    )
    search_fields = ("name", "category__name")
    list_filter = (
        "category__restaurant",
        "available",
        "menu_type",
        "category",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("table", "status", "total_price")
    list_filter = ("status", "table__restaurant")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "menu_item",
        "price_type",
        "price",
        "quantity",
        "total_price",
    )
    list_filter = ("price_type", "menu_item")
