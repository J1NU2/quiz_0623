from unicodedata import category
from django.db import models


class Category(models.Model):
    class Meta:
        db_table = "categories"

    name = models.CharField(max_length=100)


class Item(models.Model):
    class Meta:
        db_table = "items"

    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image_url = models.URLField()


class Order(models.Model):
    class Meta:
        db_table = "orders"

    delivery_address = models.CharField(max_length=100)
    order_date = models.DateTimeField()
    item = models.ManyToManyField('Item', through='ItemOrder')


class ItemOrder(models.Model):
    class Meta:
        db_table = "item_orders"

    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    item_count = models.IntegerField()
    