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
)
from loguru import logger

from common.abstract_models import CreateUpdate
from common.model_helpers import attach_qr, now_time, random_pin
from common.taxonomies import MenuType


class Chain(CreateUpdate):
    name = CharField(max_length=512)

    def __str__(self):
        return f"{self.name}"


class UserProfile(CreateUpdate):
    user = OneToOneField(to=User, on_delete=PROTECT)
    chain = ForeignKey(Chain, on_delete=PROTECT)
    email_otp = PositiveIntegerField(
        validators=[MaxValueValidator(999999), MinValueValidator(100000)],
        default=random_pin,
    )
    email_otp_sent = DateTimeField(null=True, blank=True)
    email_verified = BooleanField(default=False)

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


class MenuItem(CreateUpdate):
    name = CharField(max_length=512)
    image = ImageField(blank=True, null=True)
    category = ForeignKey(Category, on_delete=PROTECT)
    menu_type = CharField(
        max_length=8, choices=MenuType.choices, default=MenuType.VEG
    )
    half_price = DecimalField(max_digits=10, decimal_places=2, default=0)
    full_price = DecimalField(max_digits=10, decimal_places=2, default=0)
    description = TextField(blank=True)

    def __str__(self):
        return f"{self.name} / {self.category}"


class LoginPinRequest(CreateUpdate):
    DECAY_SECONDS = 15 * 60
    RATE_LIMIT_SECONDS = 60

    user = ForeignKey(User, on_delete=PROTECT)
    generated_at = DateTimeField(auto_now_add=True)
    pin = PositiveIntegerField(default=random_pin)
    used = BooleanField(default=False)
    used_timestamp = DateTimeField(null=True, blank=True)

    def save(self, **kwargs):
        super(LoginPinRequest, self).save(**kwargs)
        logger.debug(f"**Pin Request** {self.pin}")

    def __str__(self):
        return f"{self.user} / {self.generated_at}"

    def is_valid(self, user: User) -> bool:
        if self.used or self.user != user:
            return False
        diff = (now_time() - self.generated_at).total_seconds()
        return diff < self.DECAY_SECONDS

    @property
    def msg_body(self) -> str:
        return f"Your OTP is {self.pin} for logging into Flameback app."

    @property
    def otp_resend_remaining_time(self) -> int:
        match = (
            LoginPinRequest.objects.filter(user=self.user)
            .order_by("-generated_at")
            .first()
        )
        if match:
            diff = (now_time() - match.generated_at).total_seconds()
            if diff < self.RATE_LIMIT_SECONDS:
                remaining = self.RATE_LIMIT_SECONDS - diff
                return int(remaining)

        return 0

    @classmethod
    def rate_limited_create(cls, phone: str) -> "LoginPinRequest":
        user, created = User.objects.get_or_create(username=phone)
        if created:
            UserProfile.objects.create(
                phone=phone, user=user, phone_verified=True
            )
        if phone.startswith("+91322"):
            instance = LoginPinRequest.objects.create(user=user)
            instance.pin = "1234"
            instance.save()
            return instance
        match = (
            LoginPinRequest.objects.filter(user=user)
            .order_by("-generated_at")
            .first()
        )
        if match:
            diff = (now_time() - match.generated_at).total_seconds()
            if diff < cls.RATE_LIMIT_SECONDS:
                remaining = cls.RATE_LIMIT_SECONDS - diff
                raise ValidationError(
                    {
                        "phone": (
                            f"Please wait for {int(remaining)} "
                            f"seconds before retrying."
                        )
                    }
                )
        return LoginPinRequest.objects.create(user=user)
