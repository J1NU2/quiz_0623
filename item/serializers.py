from rest_framework import serializers

from item.models import Category as CategoryModel
from item.models import Item as ItemModel
from item.models import Order as OrderModel
from item.models import ItemOrder as ItemOrderModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ["name"]


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = ItemModel
        fields = ["name", "image_url", "category"]


class OrderSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=True)

    class Meta:
        model = OrderModel
        fields = ["delivery_address", "order_date", "item"]


class ItemOrderSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=True)
    order = OrderSerializer(many=True)

    class Meta:
        model = ItemOrderModel
        fields = ["item_count", "item", "order"]
        