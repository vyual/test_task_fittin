from rest_framework import serializers

from shop.models import CartItem, Category, Order, Price, Product, ProductsInOrder
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username

        return token


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "products",
            "created_at",
        ]


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "parent",
            "children",
        ]

    def get_children(self, obj):
        if obj.is_leaf_node():
            return None
        return CategorySerializer(obj.get_children(), many=True).data


class CategoryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent",]


class ProductCatalogSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        read_only=True,
    )
    old_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        read_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "price",
            "old_price",
        ]


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = [
            "id",
            "product",
            "city",
            "price",
        ]
        
        

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "products",
        ]
        read_only_fields = ['customer']

    def create(self, validated_data):
        user = self.context['request'].user
        order = Order.objects.create(customer=user, **validated_data)
        return order


class ProductsInOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsInOrder
        fields = [
            "id",
            "order",
            "product",
            "quantity",
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductCatalogSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']
        read_only_fields = ('id',)

    def create(self, validated_data):
        # Создание нового CartItem с указанным продуктом и количеством
        cart_item = CartItem.objects.create(**validated_data)
        return cart_item

    def update(self, instance, validated_data):
        # Обновление существующего CartItem
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance