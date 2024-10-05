from cloudinary import uploader
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from common.models import Table


@receiver(post_save, sender=Table)
def table_save(sender, instance: Table, **kwargs):
    if kwargs["created"]:
        instance.number = instance.restaurant.table_count
        instance.qr_code_response = uploader.upload(
            file=instance.qr_code,
            public_id=str(instance.uid),
            overwrite=True,
            folder="Waiter/Tables/QR",
        )
        instance.save()


@receiver(post_delete, sender=Table)
def table_delete(sender, instance: Table, using, **kwargs):
    if public_id := instance.qr_code_response.get("public_id", None):
        uploader.destroy(public_id=public_id)
