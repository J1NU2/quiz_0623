from rest_framework import serializers

from item.models import Category as CategoryModel
from item.models import Item as ItemModel
from item.models import Order as OrderModel
from item.models import ItemOrder as ItemOrderModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ["name"]
        # fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    # category는 ForeignKey이기 때문에 object이다.
    category = CategorySerializer()

    # 직접 커스텀하기
    # category = serializers.SerializerMethodField()
    # obj는 Item object이다.
    # def get_category(self, obj):
    #     return obj.category.name

    class Meta:
        model = ItemModel
        fields = ["id", "name", "image_url", "category", "category_id"]

    def create(self, validated_data):
        # pop : validation 내에 있는 데이터를 꺼내 오는 것
        category_data = validated_data.pop("category")
        category_name = category_data.get("name")
        category_obj = CategoryModel.object.get(name=category_name)

        item = ItemModel(category=category_obj, **validated_data)
        item.save()

        return item


class OrderSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=True)

    class Meta:
        model = OrderModel
        fields = ["delivery_address", "order_date", "item"]


class ItemOrderSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    order = OrderSerializer()
    # # item = ItemSerializer(many=True, read_only=True)
    # order = OrderSerializer(many=True, read_only=True)

    # item_name = serializers.ReadOnlyField(source="item.name")

    class Meta:
        model = ItemOrderModel
        fields = ["id", "item", "order", "item_count"]
        