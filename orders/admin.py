from django.contrib import admin

from .models import CartProducts, Carts, Orders


@admin.register(CartProducts)
class CartProductsAdmin(admin.ModelAdmin):
    list_display = ("product_name", "total_products", "total_price", "cart")


@admin.register(Carts)
class CartsAdmin(admin.ModelAdmin):
    list_display = ("owner", "final_products", "final_price", "status")


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "status", "order_date")
    list_filter = ("status", "create_date", "order_date")
