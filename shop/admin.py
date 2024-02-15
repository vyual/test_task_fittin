from django.contrib import admin

from shop.models import (
    CartItem,
    Category,
    Price,
    Product,
    ProductsInOrder,
)
from mptt.admin import DraggableMPTTAdmin

class CustomMPTTModelAdmin(DraggableMPTTAdmin):
    prepopulated_fields = {"slug": ("name",)}
    mptt_level_indent = 30

    def get_form(self, request, obj=None, **kwargs):
        form = super(CustomMPTTModelAdmin, self).get_form(request, obj, **kwargs)
        return form



admin.site.register(Category, CustomMPTTModelAdmin)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
    )
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)
    list_filter = (
        "category",
    )


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "price",
    )
    
    
@admin.register(ProductsInOrder)
class ProductsInOrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    list_filter = ('order', 'product')
    search_fields = ('order__customer__username', 'product__title')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity')
    search_fields = ('customer__username', 'product__title')
    list_filter = ('product',)