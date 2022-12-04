from rest_framework import serializers

from .models import Order, OrderProduct

from product.serializers import ProductSerializer

class MyOrderItemSerializer(serializers.ModelSerializer):    
    product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = (
            "price",
            "product",
            "quantity",
        )

class MyOrderSerializer(serializers.ModelSerializer):
    # items = MyOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "name",
            "address",
            "phone",
            "shipping",

            # "items",
            # "note",
            "order_total"
        )

class OrderItemSerializer(serializers.ModelSerializer):    
    class Meta:
        model = OrderProduct
        fields = (            
            "product",
            "quantity",
            "price",
        )



class OrderSerializer(serializers.ModelSerializer):
    print("Working on serializer")
    order_product = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "name",
            "address",
            "phone",
            "shipping",
            
            "order_product",
            "order_note",
            "order_total"
        )

    def create(self, validated_data):
        items_data = validated_data.pop('order_product')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderProduct.objects.create(order=order, **item_data)
            
        return order
    