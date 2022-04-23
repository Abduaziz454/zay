from django.db import models

from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Customer(User):
    country = models.CharField("Country", max_length=100)
    city = models.CharField("City", max_length=100)
    address = models.CharField("Address", max_length=100)
    phone = PhoneNumberField("Phone Number")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
