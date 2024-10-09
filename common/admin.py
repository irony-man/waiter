# App Imports
from django.apps import apps
from django.contrib import admin

from common.models import Category, MenuItem, Table

exclude = ["category", "table", "menuitem"]
app = apps.get_app_config("common")
for model_name, model in app.models.items():
    if model_name not in exclude:
        admin.site.register(model)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant")
    list_filter = ("restaurant",)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "restaurant")
    list_filter = ("restaurant",)
    readonly_fields = ("qr_code", "qr_code_response")


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "menu_type",
        "half_price",
        "full_price",
    )
    list_filter = ("category__restaurant", "menu_type", "category")
