from rest_framework import serializers


class AddProductSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
