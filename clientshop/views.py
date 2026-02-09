from django.db import transaction
from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from .models import Order, Product, OrderItem
from .serializers import AddProductSerializer


class AddProductToOrderView(APIView):
    """Класс для добавления товара в заказ"""

    @extend_schema(
        request=AddProductSerializer,
        responses={
            200: {"type": "object", "properties": {"status": {"type": "string"}}},
            400: {"type": "object", "properties": {"error": {"type": "string"}}},
        },
        description="Добавление товара в заказ. Если товар уже есть — увеличивает количество."
    )
    def post(self, request):
        serializer = AddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        with transaction.atomic():
            order = get_object_or_404(Order, id=data["order_id"])

            product = (
                Product.objects
                .select_for_update()
                .get(id=data["product_id"])
            )

            if product.quantity < data["quantity"]:
                return Response(
                    {"error": "Недостаточно товара на складе"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            item, created = OrderItem.objects.get_or_create(
                order=order,
                product=product,
                defaults={
                    "quantity": data["quantity"],
                    "price_at_moment": product.price
                }
            )

            if not created:
                item.quantity += data["quantity"]
                item.save()

            product.quantity -= data["quantity"]
            product.save()

        return Response({"status": "ok"})
