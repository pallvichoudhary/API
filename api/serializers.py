from rest_framework import serializers
from .models import Product, Order, OrderItem, User, models

class ProductSerializer(serializers.ModelSerializer):
        class Meta:
              model = Product
              fields =(
                     'id',
                     'name',
                     'price',
                     'stock',
              )

        def validate_price(self,value):
               if value <= 0:
                      raise serializers.ValidationError(
                             "Price must be greater than 0."
                      )
               return value
       
class UserSerializer(serializers.ModelSerializer):
       class Meta:
              model= User
              fields=(
                     'username',
                     'id'
              )

class OrderItemSerializer(serializers.ModelSerializer):
       product=ProductSerializer()
       # product_name=serializers.CharField(source='product.name',read_only=True)
       product_name = serializers.CharField(source='product.name', read_only=True)
       product_price = serializers.DecimalField(
       max_digits=10,
       decimal_places=2,
       source='product.price'  # ✅ corrected here
)
       def get_product_name(self, obj):
          return obj.product.name


       
       class Meta:
            model=OrderItem
            fields=(
                   'product_name',
                   'product_price',
                   'product',
                   'order',
                   'quantity',
                   'item_subtotal'
            )


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True,read_only=True)
    total_price=serializers.SerializerMethodField(method_name='total')
    user=UserSerializer()

        
    def total(self,obj):
       order_items=obj.items.all()
       return sum(order_item.item_subtotal for order_item in order_items)

       
    class Meta:
        model=Order
        fields = (
                     'order_id',
                     'created_at',
                     'user',
                     'status',
                     'items',
                     'total_price',
              )
        
class OrderItemCreateSerializer(serializers.ModelSerializer):
       class OrderItemCreateSerializer(serializers.ModelSerializer):
              class Meta:
                  model= OrderItem
                  fields=('product','quantity')

       order_id = serializers.UUIDField(read_only=True)
       items = OrderItemCreateSerializer(many=True)

       def create(self,validated_data):
              Orderitem_data=validated_data.pop('items')
              order = Order.objects.create(**validated_data)

              for item in Orderitem_data:
                     OrderItem.objects.create(order=order,**item)
                     return order 

       class Meta:
              model=Order
              fields=(
              'order_id',
              'user',
              'status',
              'items',
       )

       extra_kwargs={
            'user': {'read_only': True}
       }
      





class ProductInfoSerializer(serializers.Serializer):
      products=ProductSerializer(many=True)
      count=serializers.IntegerField()
      max_price=serializers.FloatField()

