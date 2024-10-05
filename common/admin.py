# App Imports
from django.apps import apps
from django.contrib import admin

from common.models import Category

exclude = [
    "category",
]
app = apps.get_app_config("common")
for model_name, model in app.models.items():
    if model_name not in exclude:
        admin.site.register(model)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant")
    list_filter = ("restaurant",)
