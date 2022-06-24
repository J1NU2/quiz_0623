from unicodedata import category
from django.db import models


# 제품 카테고리
class Category(models.Model):
    class Meta:
        db_table = "categories"

    name = models.CharField(max_length=100)


# 제품
class Item(models.Model):
    class Meta:
        db_table = "items"

    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image_url = models.URLField()


# 사람(?)
class Order(models.Model):
    class Meta:
        db_table = "orders"

    delivery_address = models.CharField(max_length=100)
    order_date = models.DateTimeField()
    item = models.ManyToManyField('Item', through='ItemOrder')


# 제품 및 사람(?) 간 중간 테이블(피벗 테이블)
class ItemOrder(models.Model):
    class Meta:
        db_table = "item_orders"

    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    item_count = models.IntegerField()
    