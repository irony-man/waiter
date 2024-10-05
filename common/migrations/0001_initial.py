# Generated by Django 5.1.1 on 2024-10-05 10:40

import uuid

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import common.model_helpers


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=512)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Chain",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=512)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="LoginPinRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("generated_at", models.DateTimeField(auto_now_add=True)),
                (
                    "pin",
                    models.PositiveIntegerField(
                        default=common.model_helpers.random_pin
                    ),
                ),
                ("used", models.BooleanField(default=False)),
                (
                    "used_timestamp",
                    models.DateTimeField(blank=True, null=True),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MenuItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=512)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                (
                    "menu_type",
                    models.CharField(
                        choices=[("VEG", "Veg"), ("NON_VEG", "Non Veg")],
                        default="VEG",
                        max_length=8,
                    ),
                ),
                (
                    "half_price",
                    models.DecimalField(
                        decimal_places=2, default=0, max_digits=10
                    ),
                ),
                (
                    "full_price",
                    models.DecimalField(
                        decimal_places=2, default=0, max_digits=10
                    ),
                ),
                ("description", models.TextField(blank=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="common.category",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Restaurant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=512)),
                (
                    "chain",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="common.chain",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="category",
            name="restaurant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="common.restaurant",
            ),
        ),
        migrations.CreateModel(
            name="Table",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("number", models.PositiveIntegerField()),
                ("qr_code", models.ImageField(upload_to="")),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="common.restaurant",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "email_otp",
                    models.PositiveIntegerField(
                        default=common.model_helpers.random_pin,
                        validators=[
                            django.core.validators.MaxValueValidator(999999),
                            django.core.validators.MinValueValidator(100000),
                        ],
                    ),
                ),
                (
                    "email_otp_sent",
                    models.DateTimeField(blank=True, null=True),
                ),
                ("email_verified", models.BooleanField(default=False)),
                (
                    "chain",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="common.chain",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
