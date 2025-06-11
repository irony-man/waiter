import logging
from tkinter import Menu

import pandas as pd
from django.core.management import BaseCommand
from loguru import logger

from common.models import MenuItem


class Command(BaseCommand):
    help = "Imports menu items"

    def add_arguments(self, parser):
        parser.add_argument("--id", dest="restaurant_id", help="Restaurant ID")

    def handle(self, *args, **options):
        restaurant_id = options.get("restaurant_id")
        if not restaurant_id:
            raise ValueError("No restaurant id was passed!!")
        queryset = MenuItem.objects.filter(
            category__restaurant_id=restaurant_id
        ).values(
            "uid",
            "name",
            "description",
            "ingredients",
            "category__name",
            "menu_type",
            "full_price",
        )
        df = pd.DataFrame(queryset)
        df.to_csv(f"menu_{restaurant_id}.csv", index=False)
        logger.info(
            f"Menu items for restaurant {restaurant_id} exported successfully to menu_{restaurant_id}.csv"
        )
