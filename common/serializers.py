from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common.models import (
    Category,
    Chain,
    MenuItem,
    Order,
    Restaurant,
    Table,
    UserProfile,
)
from common.taxonomies import MenuType, serialize


class SerializedRelationField(serializers.Field):
    def __init__(
        self, lookup_key: str, queryset: QuerySet, repr_serializer, **kwargs
    ):
        self.lookup_key = lookup_key
        self.queryset = queryset
        self.repr_serializer = repr_serializer
        super(SerializedRelationField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            value = data
            if isinstance(data, dict):
                key = self.lookup_key.split("__")[-1]
                value = data[key]
            if value:
                return self.queryset.get(**{self.lookup_key: value})
        except Exception as exc:
            raise ValidationError(exc)
        else:
            return None

    def to_representation(self, value):
        return self.repr_serializer(instance=value, context=self.context).data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]


class ChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chain
        fields = [
            "name",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.CharField(source="user.email")
    chain_name = serializers.CharField(source="chain.name")
    is_staff = serializers.BooleanField(source="user.is_staff", read_only=True)
    raw_password = serializers.CharField(write_only=True, required=False)
    choices = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "full_name",
            "username",
            "email",
            "email_verified",
            "uid",
            "chain_name",
            "created",
            "updated",
            "choices",
            "is_staff",
            "raw_password",
        ]

    def get_choices(self, instance):
        choices = {
            "menu_type": serialize(MenuType),
        }
        return choices

    def validate(self, attrs):
        if "request" in self.context:
            user_instance = self.context["request"].user
            user = User(**attrs.get("user"))
            if user_instance.username != user.username:
                user.validate_unique()
        return super(UserProfileSerializer, self).validate(attrs)

    def create(self, validated_data):
        user = User(**validated_data.pop("user"))
        user.set_password(raw_password=validated_data.pop("raw_password"))
        instance = UserProfile(**validated_data)
        instance.user = user
        user.save()
        instance.save()
        return instance

    def update(self, instance, validated_data):
        if "request" in self.context:
            user_instance = self.context["request"].user
            user = User(**validated_data.pop("user"))
            instance.user.username = user.username
            instance.user.email = user.email
            instance.user.save()
            if "raw_password" in validated_data:
                user_instance.set_password(
                    raw_password=validated_data.pop("raw_password")
                )
                user_instance.save()

        return super(UserProfileSerializer, self).update(
            instance, validated_data
        )


class LiteUserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "display_picture_url",
            "username",
            "email",
            "uid",
        ]


class RestaurantSerializer(serializers.ModelSerializer):
    chain = ChainSerializer(read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            "uid",
            "name",
            "chain",
            "table_count",
            "category_count",
            "created",
            "updated",
        ]


class TableSerializer(serializers.ModelSerializer):
    restaurant = SerializedRelationField(
        "uid", Restaurant.objects, RestaurantSerializer
    )
    number = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Table
        fields = [
            "uid",
            "number",
            "restaurant",
            "qr_code_url",
            "created",
            "updated",
        ]


class CategorySerializer(serializers.ModelSerializer):
    restaurant = SerializedRelationField(
        "uid", Restaurant.objects, RestaurantSerializer
    )

    class Meta:
        model = Category
        fields = [
            "uid",
            "name",
            "restaurant",
            "image",
            "created",
            "updated",
        ]


class LiteCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "uid",
            "name",
        ]


class MenuItemSerializer(serializers.ModelSerializer):
    category = SerializedRelationField(
        "uid", Category.objects, LiteCategorySerializer
    )

    class Meta:
        model = MenuItem
        fields = [
            "uid",
            "name",
            "image",
            "category",
            "menu_type",
            "available",
            "half_price",
            "full_price",
            "description",
            "created",
            "updated",
        ]


class LiteMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = [
            "uid",
            "name",
            "image",
            "menu_type",
            "available",
            "half_price",
            "full_price",
            "description",
        ]


class OrderSerializer(serializers.ModelSerializer):
    menu_item = SerializedRelationField(
        "uid", MenuItem.objects.filter(available=True), LiteMenuItemSerializer
    )
    table = SerializedRelationField(
        "uid", Table.objects, TableSerializer, write_only=True
    )
    price = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )
    total_price = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "uid",
            "menu_item",
            "table",
            "price",
            "total_price",
            "price_type",
            "quantity",
            "status",
            "session_uid",
        ]

    def validate(self, attrs):
        instance = Order(**attrs)
        instance.clean()
        return super(OrderSerializer, self).validate(attrs)


class LiteOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "uid",
            "status",
        ]
