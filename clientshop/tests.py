# from django.test import TestCase
# Create your tests here.
# from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from clientshop.models import Category, Client, Order, OrderItem, Product


class AddProductToOrderAPITest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Root")
        self.product = Product.objects.create(
            name="Test Product", quantity=10, price=100, category=self.category
        )
        self.client_obj = Client.objects.create(
            name="Test Client", address="Test address"
        )
        self.order = Order.objects.create(client=self.client_obj)

        self.url = "/api/add-product/"

    def test_add_new_product_to_order(self):
        response = self.client.post(
            self.url,
            {"order_id": self.order.id, "product_id": self.product.id, "quantity": 3},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(OrderItem.objects.count(), 1)

        item = OrderItem.objects.first()
        self.assertEqual(item.quantity, 3)

        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 7)

    def test_add_existing_product_increases_quantity(self):
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price_at_moment=self.product.price,
        )

        response = self.client.post(
            self.url,
            {"order_id": self.order.id, "product_id": self.product.id, "quantity": 3},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(OrderItem.objects.count(), 1)

        item = OrderItem.objects.first()
        self.assertEqual(item.quantity, 5)

        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 7)

    def test_not_enough_product_quantity(self):
        response = self.client.post(
            self.url,
            {"order_id": self.order.id, "product_id": self.product.id, "quantity": 50},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(OrderItem.objects.count(), 0)

        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 10)
