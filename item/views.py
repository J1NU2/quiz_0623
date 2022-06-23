from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from item.models import Item as ItemModel

from item.serializers import CategorySerializer
from item.serializers import ItemSerializer
from item.serializers import OrderSerializer
from item.serializers import ItemOrderSerializer


class ItemView(APIView):
    def get(self, request):
        category = ItemModel.objects.filter(category=request.data)
        return Response(ItemSerializer)
