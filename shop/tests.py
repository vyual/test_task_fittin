from django.urls import reverse
from rest_framework.test import APITestCase
from account.models import CustomUser
from shop.models import CartItem, Category, Product, Order, Price, ProductsInOrder
import unittest
from rest_framework import status


class ProductViewSetTests(APITestCase):
    # Тесты для ProductViewSet
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='admin', password='admin123', is_staff=True)
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(title="Laptop", description="A powerful laptop.", slug="laptop", category=self.category)
        Price.objects.create(product=self.product, price=1000.00)

    def test_list_products(self):
        self.client.login(username='admin', password='admin123')
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CategoryViewSetTests(APITestCase):
    # Тесты для CategoryViewSet

    def setUp(self):
        self.category = Category.objects.create(name="Books", slug="books")

    def test_list_categories(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_category(self):
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

class OrderCreationTests(APITestCase):
    # Тесты для CartItemViewSet
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='customer', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="Clothing", slug="clothing")
        self.product = Product.objects.create(title="T-Shirt", description="A cool t-shirt.", slug="t-shirt", category=self.category)
        self.cart_item = CartItem.objects.create(customer=self.user, product=self.product, quantity=1)

    def test_create_order_from_cart_items(self):
        response = self.client.post(reverse('order-list'), {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, был ли создан заказ
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(ProductsInOrder.objects.count(), 1)

        # Проверяем, пуста ли корзина после создания заказа
        self.assertEqual(CartItem.objects.filter(customer=self.user).count(), 0)


if __name__ == '__main__':
    unittest.main()
