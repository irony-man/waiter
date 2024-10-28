from django.core.management import BaseCommand

from common.tasks import import_menu_items


class Command(BaseCommand):
    # To run:
    # ./manage.py import_menu --file <path>
    help = "Imports menu items"

    def add_arguments(self, parser):
        parser.add_argument("--id", dest="restaurant_id", help="Restaurant ID")

    def handle(self, *args, **options):
        import_menu_items(options["restaurant_id"])
