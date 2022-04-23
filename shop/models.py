from django.db import models
from accounts.models import Customer

from polymorphic.models import PolymorphicModel

import geocoder


mapbox_access_token = 'pk.eyJ1IjoiYWJkdWF6aXoiLCJhIjoiY2t6bnFtZmxoMDljYzJ2cWdqOXc5NHJtMSJ9.2bquCt0JhPU3o3FYSPP8Hw'


class ProductReviews(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, verbose_name="Продукт")
    author = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Автор")
    body = models.CharField("Содержимое", max_length=100)

    def __str__(self):
        return f"Продукт: {self.product.title} Автор: {self.author.username}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


class ProductImages(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, verbose_name="Продукт")
    image = models.ImageField("Картинка", upload_to="product-images/")

    def __str__(self):
        return f"Картинка продукта: {self.product.pk}"

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"


class Product(PolymorphicModel):
    title = models.CharField("Title", max_length=100)
    description = models.CharField("Description", max_length=255)
    count_views = models.PositiveSmallIntegerField("Count Views", default=0)
    price = models.DecimalField("Price", max_digits=12, decimal_places=2)
    image = models.ImageField("Image", upload_to="product-images/")
    brand = models.CharField("Brand", max_length=255, null=True)
    time_create = models.DateTimeField("Time Create", auto_now_add=True)
    time_update = models.DateTimeField("Time Update", auto_now=True)
    is_published = models.BooleanField("Published", default=True)

    def get_ct_model_name(self):
        return self.__class__.__name__.lower()


    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-pk"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

class MenClothes(Product):
    SIZE_CHOICES_DEFAULT = "S"
    SIZE_CHOICES = [
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
    ]

    size = models.CharField("Size", max_length=50, choices=SIZE_CHOICES, default=SIZE_CHOICES_DEFAULT)
    country = models.CharField("Country", max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Men's Clothes"
        verbose_name_plural = "Men's Clothes"



class WomenClothes(Product):
    SIZE_CHOICES_DEFAULT = "S"
    SIZE_CHOICES = [
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
    ]

    size = models.CharField("Size", max_length=50, choices=SIZE_CHOICES, default=SIZE_CHOICES_DEFAULT)
    country = models.CharField("Country", max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Women's Clothes"
        verbose_name_plural = "Women's Clothes"


class Gadgets(Product):
    company = models.CharField("Company", max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Gadget"
        verbose_name_plural = "Gadgets"


class Followers(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Mailing list"
        verbose_name_plural = "Mailing lists"

class Mail_Contacts(models.Model):
    email = models.EmailField("Email", unique=True)
    name = models.CharField("Name", max_length=100)
    subject = models.CharField("Subject", max_length=20, null=True, blank=True)
    message = models.CharField("Message", max_length=255)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

class Address(models.Model):
    title = models.CharField("Title", max_length=100)
    address = models.TextField("Address")
    lat = models.FloatField("Latitude", blank=True, null=True)
    long = models.FloatField("Longitude", blank=True, null=True)

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address, key=mapbox_access_token)
        g = g.latlng
        self.lat = g[0]
        self.long = g[1]
        return super(Address, self).save(*args, **kwargs)