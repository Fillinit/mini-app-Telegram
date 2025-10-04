from rest_framework import serializers
from .models import Catalog, Product, ProductOption, Order, OrderItem

class CatalogSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Catalog
        fields = ['id', 'name', 'actual', 'products_count', 'created_at']
    
    def get_products_count(self, obj):
        return obj.products.count()


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    options = ProductOptionSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product','quantity','price','options']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','telegram_user_id','status','total','address','items']


    def create(self, validated_data):
        items = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        total = 0
        for it in items:
            prod = it['product']
            qty = it.get('quantity',1)
            price = it.get('price', prod.price)
            OrderItem.objects.create(order=order, product=prod, quantity=qty, price=price, options=it.get('options',{}))
            total += price * qty
            order.total = total
            order.save()
        return order