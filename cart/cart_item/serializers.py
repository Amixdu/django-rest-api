from rest_framework import serializers
from . import models


class CartItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    price = serializers.FloatField()
    quantity = serializers.IntegerField(required=False, default=1)

    class Meta:
        model = models.CartItem
        fields = "__all__"
