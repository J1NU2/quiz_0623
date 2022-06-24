from datetime import timedelta
from time import time
from django.db.models.query_utils import Q
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from item.models import Category as CategoryModel
from item.models import Item as ItemModel
from item.models import Order as OrderModel

from item.serializers import CategorySerializer
from item.serializers import ItemSerializer
from item.serializers import OrderSerializer
from item.serializers import ItemOrderSerializer


class ItemView(APIView):
    def get(self, request):
        # GET 요청으로 category에 대한 것 불러오기
        category = request.GET.get("category", "")
        # category = request.GET["category"]

        # request로 인한 category를 가지고 CategoryModel에서 name을 찾기
        category_str = CategoryModel.objects.get(name=category)

        # 요청(request)과 일치하는 값을 CategoryModel에서 찾는다.
        # 해당 값과 같은 것을 filter를 통해 ItemModel에서 찾는다.
        items = ItemModel.objects.filter(category=category_str)

        return Response(ItemSerializer(items, many=True).data)

    def post(self, request):
        # serializer 미사용
        # data = request.data # 입력받은 item 정보 저장
        # item = ItemModel.objects.create(**data)
        # item.save()

        # serializer 사용
        items = ItemSerializer(data=request.data)

        if items.is_valid:
            items.save()

            return Response({"success": "등록 완료"}, status=status.HTTP_200_OK)

        return Response({"fail": "등록 실패"}, status=status.HTTP_400_BAD_REQUEST)


class OrderView(APIView):
    def get(self, request):
        # order의 id 가져오기
        order_id = request.GET.get("order_id")

        # 일주일 전 = 7일 전
        seven_days_ago = timezone.now() - timedelta(days=7)

        # 조건 부여(Q)
        # gt : 크다(>)
        # lt : 작다(<)
        # gte : 크거나 같다(>=)
        # lte : 작거나 같다(<=)
        terms = Q(id=order_id) & Q(order_date__gte=seven_days_ago)

        # get으로 사용할 때
        # 해당 값이 없으면 error가 발생할 수 있다.
        # 이때, error를 관리하기 위해서 try-except를 사용해서 예외처리를 해주면 좋다.
        order_obj = OrderModel.objects.get(terms)

        return Response(OrderSerializer(order_obj).data)

        # 만약 objects.filter 라면?
        # filter로 사용하게 되면 queryset으로 찾는 것이기 때문에 many=Ture를 같이 써줘야 한다.
        # order_obj = OrderModel.objects.filter(terms)
        # return Response(OrderSerializer(order_obj, many=True).data)
