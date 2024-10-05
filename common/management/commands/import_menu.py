import json

from django.core.management import BaseCommand
from django.db import transaction
from loguru import logger

from common.models import Category, MenuItem


class Command(BaseCommand):
    # To run:
    # ./manage.py import_questions --file <path>
    help = "Imports menu items"

    def add_arguments(self, parser):
        parser.add_argument("--file", dest="file", help="Menu json file")
        parser.add_argument("--id", dest="restaurant_id", help="Restaurant ID")

    def handle(self, *args, **options):
        with open(options["file"]) as f:
            data = json.load(f)
            with transaction.atomic():
                for category_row in data:
                    category = Category.objects.create(
                        name=category_row["category"],
                        restaurant_id=options["restaurant_id"],
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
