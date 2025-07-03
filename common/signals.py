from django.db.models.signals import post_save
from django.dispatch import receiver

from common.models import Table


@receiver(post_save, sender=Table)
def table_save(sender, instance: Table, **kwargs):
    if kwargs["created"]:
        instance.number = instance.restaurant.table_count
        instance.save()
