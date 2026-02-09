from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Order, Product, OrderItem
from .serializers import AddProductSerializer


class AddProductToOrderView(APIView):

    def post(self, request):
        serializer = AddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data["order_id"]
        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]

        order = Order.objects.get(id=order_id)
        product = Product.objects.get(id=product_id)

        if product.quantity < quantity:
            return Response(
                {"error": "Недостаточно товара на складе"},
                status=status.HTTP_400_BAD_REQUEST
            )

        item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={
                "quantity": quantity,
                "price_at_moment": product.price
            }
        )

        if not created:
            item.quantity += quantity
            item.save()

        product.quantity -= quantity
        product.save()

        return Response({"status": "ok"})
