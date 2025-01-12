from cloudinary import uploader  # type: ignore
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


# @receiver(post_save, sender=Order)
# def order_save(sender, instance: Order, created, **kwargs):
#     if created:
#         return
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         str(instance.session_uid),
#         {
#             "type": "send_order",
#             "order": instance,
#         },
#     )
#     async_to_sync(channel_layer.group_send)(
#         str(instance.table.restaurant.uid),
#         {
#             "type": "send_order",
#             "order": instance,
#         },
#     )


# @receiver(post_save, sender=OrderItem)
# def order_item_save(sender, instance: OrderItem, created, **kwargs):
#     if created:
#         return
#     channel_layer = get_channel_layer()
#     order: Order = instance.order
#     async_to_sync(channel_layer.group_send)(
#         str(order.session_uid),
#         {
#             "type": "send_order",
#             "order": order,
#         },
#     )
#     async_to_sync(channel_layer.group_send)(
#         str(order.table.restaurant.uid),
#         {
#             "type": "send_order",
#             "order": order,
#         },
#     )
