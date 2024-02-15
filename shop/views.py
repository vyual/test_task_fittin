from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework import permissions, status, viewsets
from shop.models import CartItem, Category, Order, Price, Product, ProductsInOrder

from shop.serializers import CartItemSerializer, CategoryDetailSerializer, CategorySerializer, MyTokenObtainPairSerializer, OrderSerializer, ProductCatalogSerializer

from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.db.models import Q, Subquery, OuterRef
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db import transaction
from rest_framework.permissions import IsAuthenticated  


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ReadOnlyOrAdminPermission(permissions.BasePermission):
    """
    Разрешение, которое позволяет только чтение для всех пользователей, но полный доступ для администраторов.
    """

    def has_permission(self, request, view):
        # Проверка, является ли пользователь администратором
        if request.user and request.user.is_staff:
            return True

        # Проверка типа запроса: разрешить только запросы на чтение
        return request.method in permissions.SAFE_METHODS


class ProductViewSet(viewsets.ModelViewSet):
    """
    Возвращает товары с учетом цены в заданном городе.
    """

    queryset = Product.objects.all().order_by("-created_at")
    permission_classes = [ReadOnlyOrAdminPermission]
    serializer_class = ProductCatalogSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="price_gte",
                type=float,
                location=OpenApiParameter.QUERY,
                description="Фильтр цены: больше или равно",
            ),
            OpenApiParameter(
                name="price_lte",
                type=float,
                location=OpenApiParameter.QUERY,
                description="Фильтр цены: меньше или равно",
            ),
            OpenApiParameter(
                name="category",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Фильтр по категории (SLUG)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        price_lte = request.query_params.get("price_lte")
        price_gte = request.query_params.get("price_gte")
        category = request.query_params.get("category")
        
        filter_conditions = Q()
        price_filter_applied = False

        if price_gte or price_lte:
            price_filter = Price.objects.filter(product=OuterRef("pk"))
            price_filter_applied = True
            if price_lte is not None:
                price_filter = price_filter.filter(price__lte=price_lte)
            if price_gte is not None:
                price_filter = price_filter.filter(price__gte=price_gte)

            self.queryset = self.queryset.annotate(
                price=Subquery(price_filter.values("price")[:1]),
                old_price=Subquery(price_filter.values("old_price")[:1]),
            )
            
            if not self.queryset.filter(Q(id__in=Subquery(price_filter.values("product")))).exists():
                return Response([])  # Возвращаем пустой ответ, если по фильтру цены нет совпадений

        if category:
            filter_conditions &= Q(category__slug=category) | Q(additional_categories__slug=category)
            filtered_queryset = self.queryset.filter(filter_conditions)
            if not filtered_queryset.exists() and price_filter_applied:
                return Response([])  # Возвращаем пустой ответ, если по фильтру категории нет совпадений и был применен фильтр цены
            elif filtered_queryset.exists():
                self.queryset = filtered_queryset

        return super().list(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnlyOrAdminPermission]

    def get_serializer_class(self):
        if self.action in ["retrieve"]:
            return CategoryDetailSerializer
        return super().get_serializer_class()



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        customer = request.user
        cart_items = CartItem.objects.filter(customer=customer)

        if not cart_items.exists():
            return Response({"error": "Корзина пуста."}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            order = Order.objects.create(customer=customer)
            for item in cart_items:
                ProductsInOrder.objects.create(order=order, product=item.product, quantity=item.quantity)
                item.delete()  # Удаление товара из корзины после добавления в заказ

            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)        
        

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
