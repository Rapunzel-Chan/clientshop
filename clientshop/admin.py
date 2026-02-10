from django.contrib import admin

from clientshop.models import Category, Client, Order, OrderItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity", "category", "price")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "address")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("client", "created_at")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price_at_moment")
