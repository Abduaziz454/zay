from django.db.models import Sum

from .models import CartProducts


def recalc_cart(cart):
    cart_products = CartProducts.objects.filter(cart_id=cart.pk)
    result = cart_products.aggregate(Sum("total_products"), Sum("total_price"))
    cart.final_price = result["total_price__sum"]
    cart.final_products = result["total_products__sum"]
    cart.save()
