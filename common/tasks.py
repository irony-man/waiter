import json

from django.db import transaction
from loguru import logger

from common.models import Category, MenuItem


def import_menu_items(restaurant_id):
    if not restaurant_id:
        raise ValueError("No restaurant id was passed!!")
    with open("./fixtures/menu.json") as f:
        data = json.load(f)
        with transaction.atomic():
            for category_row in data:
                category = Category.objects.create(
                    name=category_row["category"],
                    restaurant_id=restaurant_id,
                )
                for item in category_row["items"]:
                    MenuItem.objects.create(
                        name=item["name"],
                        full_price=item["full_price"],
                        category=category,
                    )
                    logger.info(
                        f"{item['name']} of category {category.name} is generated."
                    )
