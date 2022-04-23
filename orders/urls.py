from django.urls import path

from . import views

urlpatterns = [
    path("cart/", views.CartView.as_view(), name="cart_view"),
    path("add-cart/<str:ct_model>/<int:product_pk>/", views.AddCartProductView.as_view(), name="add_cart"),
    path("make-order/", views.MakeOrder.as_view(), name="make_order"),

]