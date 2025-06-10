# # Standard Library
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    PROTECT,
    BooleanField,
    CharField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    ImageField,
    JSONField,
    OneToOneField,
    PositiveIntegerField,
    TextField,
    UUIDField,
)
from loguru import logger

from common.abstract_models import CreateUpdate
from common.model_helpers import attach_qr, now_time, random_pin
from common.taxonomies import MenuType, OrderStatus, PriceType


class Chain(CreateUpdate):
    name = CharField(max_length=512)

    def __str__(self):
        return f"{self.name}"


class UserProfile(CreateUpdate):
    user = OneToOneField(to=User, on_delete=PROTECT)
    chain = ForeignKey(Chain, on_delete=PROTECT)
    is_guest = BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} / {self.user}"

    @property
    def full_name(self):
        return self.user.get_full_name()

    # def request_password_reset(self):
    #     now = timezone.now()
    #     delta = now - timedelta(minutes=10)
    #     recent = PasswordResetRequest.objects.filter(
    #         user=self.user, created__range=(delta, now)
    #     )
    #     if recent.exists():
    #         logger.info("Request less than 10 minutes old exists.")
    #         return
    #     PasswordResetRequest.objects.create(user=self.user)


class Restaurant(CreateUpdate):
    name = CharField(max_length=512)
    chain = ForeignKey(Chain, on_delete=PROTECT)

    @property
    def table_count(self):
        return self.table_set.count()

    @property
    def category_count(self):
        return self.category_set.count()

    def __str__(self):
        return f"{self.name} / {self.chain}"


class Table(CreateUpdate):
    number = PositiveIntegerField(default=0)
    restaurant = ForeignKey(Restaurant, on_delete=PROTECT)
    qr_code = ImageField()
    qr_code_response = JSONField(default=dict, blank=True)

    def qr_code_url(self):
        return self.qr_code_response.get("secure_url", None)

    def __str__(self):
        return f"{self.number} / {self.restaurant}"

    def save(self, **kwargs):
        if not self.qr_code:
            self.qr_code = ImageFile(
                attach_qr(self.uid), name=f"QR_{self.uid}.png"
            )
        super(Table, self).save(**kwargs)


class Category(CreateUpdate):
    name = CharField(max_length=512)
    restaurant = ForeignKey(Restaurant, on_delete=PROTECT)
    image = ImageField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} / {self.restaurant}"

    class Meta:
        verbose_name_plural = "Categories"


class MenuItem(CreateUpdate):
    name = CharField(max_length=512)
    image = ImageField(blank=True, null=True)
    category = ForeignKey(Category, on_delete=PROTECT)
    menu_type = CharField(
        max_length=8, choices=MenuType.choices, default=MenuType.VEG
    )
    available = BooleanField(default=True)
    half_price = DecimalField(max_digits=10, decimal_places=2, default=0)
    full_price = DecimalField(max_digits=10, decimal_places=2, default=0)
    description = TextField(blank=True)
    ingredients = TextField(blank=True)

    def __str__(self):
        return f"{self.name} / {self.category}"


class Order(CreateUpdate):
    session_uid = UUIDField()
    table = ForeignKey(Table, on_delete=PROTECT)
    status = CharField(
        choices=OrderStatus.choices, default=OrderStatus.PENDING, max_length=32
    )

    @property
    def status_display(self):
        return self.get_status_display()

    @property
    def total_price(self):
        return sum(i.total_price for i in self.orderitem_set.all())

    def __str__(self):
        return f"{self.table} / {self.status}"


class OrderItem(CreateUpdate):
    order = ForeignKey(Order, on_delete=PROTECT)
    menu_item = ForeignKey(MenuItem, on_delete=PROTECT)
    price_type = CharField(
        choices=PriceType.choices, default=PriceType.FULL, max_length=8
    )
    quantity = PositiveIntegerField()

    @property
    def price(self):
        return (
            self.menu_item.full_price
            if self.price_type == PriceType.FULL
            else self.menu_item.half_price
        )

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.order} / {self.menu_item} / {self.quantity}"

    def clean(self):
        if self.order.table.restaurant != self.menu_item.category.restaurant:
            raise ValidationError({"table": "Table not found."})
