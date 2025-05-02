from rest_framework import serializers
from .models import Product, Order, OrderItem, CheckoutLog

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')

    class Meta:
        model = Order
        fields = ['id', 'customer', 'date_ordered', 'complete', 'items']

class CheckoutLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckoutLog
        fields = '__all__'
