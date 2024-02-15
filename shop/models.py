from django.db import models
from django.urls import reverse

from account.models import CustomUser, TimeBasedModel

from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

class Category(MPTTModel, TimeBasedModel):
    name = models.CharField(
        max_length=255,
        verbose_name="Категория",
    )

    slug = models.SlugField(unique=True, max_length=256)

    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Каталог",
    )
    is_visible = models.BooleanField(
        verbose_name="Видна ли категория (ВЕЗДЕ)",
        default=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("-id",)

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name



class Product(TimeBasedModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Каноническая категория",
    )
    additional_categories = models.ManyToManyField(
        Category,
        related_name="additional_products",
        verbose_name="Дополнительные категории",
        blank=True,
    )

    title = models.CharField(
        max_length=255,
        verbose_name="Наименование",
    )

    description = models.TextField(verbose_name="Описание")

    slug = models.SlugField(unique=True, max_length=256)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title


class Price(TimeBasedModel):
    product = models.ForeignKey(
        Product, related_name="prices", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Старая цена (для скидки)",
        null=True,
    )

    class Meta:
        verbose_name = "Цена"
        verbose_name_plural = "Цены"
        unique_together = ("product", )

    def __str__(self):
        return f"{self.product.title}: {self.price}"


class Order(TimeBasedModel):
    customer = models.ForeignKey(
        CustomUser,
        related_name="customer",
        on_delete=models.CASCADE,
        verbose_name="Покупатель",
    )
    products = models.ManyToManyField(
        Product, verbose_name="Товары", blank=True, through="ProductsInOrder"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"{self.customer} - {self.created_at}"


class ProductsInOrder(TimeBasedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name="Товар",
        related_name="count_in_order",
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name="Количество товара в заказе"
    )

    def __str__(self) -> str:
        return f"Корзина {self.id}"
    

class CartItem(TimeBasedModel):
    customer = models.OneToOneField(CustomUser, related_name="cart", on_delete=models.CASCADE, verbose_name="Покупатель")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    
    
    class Meta:
        verbose_name = "Продукт в корзине пользователя"
        verbose_name_plural = "Продукт в корзине пользователя"