from django.db import models
from django.utils import timezone

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from accounts.models import Customer


class CartProducts(models.Model):
    cart = models.ForeignKey("Carts", on_delete=models.CASCADE, verbose_name="Cart")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    product_id = models.PositiveSmallIntegerField()
    product = GenericForeignKey("content_type", "product_id")

    product_name = models.CharField("Product Name", max_length=100)
    total_products = models.PositiveSmallIntegerField("Total Products", default=0)
    total_price = models.DecimalField("Total Price", max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "Product on Cart"
        verbose_name_plural = "Products on Cart"


class Carts(models.Model):
    STATUS_DEFAULT = "New Cart"
    STATUS_CHOICES = [
        ("new", "New Cart"),
        ("in_process", "In Process"),
        ("in_order", "In Order")
    ]

    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Owner")
    final_products = models.PositiveSmallIntegerField("Final Products", default=0)
    final_price = models.DecimalField("Final Price", max_digits=12, decimal_places=2, default=0)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default=STATUS_DEFAULT)

    def __str__(self):
        return f"Cart № {self.pk}/ Owner: {self.owner.first_name} {self.owner.last_name}"

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

class Orders(models.Model):
    DELIVER_TYPE_DEFAULT = "Доставка"
    DELIVER_TYPE_CHOICES = [
        ("deliver", "Deliver"),
        ("self", "Self")
    ]

    STATUS_DEFAULT = "New Order"
    STATUS_CHOICES = [
        ("new", "New Order"),
        ("in_deliver", "In deliver"),
        ("completed", "Completed"),
        ("denied", "Denied")
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Customer")
    cart = models.ForeignKey(Carts, on_delete=models.CASCADE, verbose_name="Cart")

    first_name = models.CharField("First Name", max_length=150)
    last_name = models.CharField("Last Name", max_length=150)
    country = models.CharField("Country", max_length=100)
    city = models.CharField("City", max_length=100)
    address = models.CharField("Address", max_length=100)
    phone = models.CharField("Phone", max_length=100)
    email = models.EmailField("Email", blank=True)
    deliver_type = models.CharField("Deliver Type", max_length=10, choices=DELIVER_TYPE_CHOICES,
                                    default=DELIVER_TYPE_DEFAULT)
    status = models.CharField("Status", max_length=12, choices=STATUS_CHOICES,
                              default=STATUS_DEFAULT)
    create_date = models.DateTimeField("Create Date", auto_now_add=True)
    order_date = models.DateField("Order Date", default=timezone.now)

    def __str__(self):
        return f"Заказ № {self.pk}/ Покупатель: {self.customer.first_name} {self.customer.last_name}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"