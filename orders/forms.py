from django import forms
from django.utils import timezone

from .models import Orders


class OrdersForm(forms.ModelForm):
    order_date = forms.DateField(label="Дата доставки", widget=forms.DateInput({
        "type": "date",
        "min": timezone.now().date()
    }))

    class Meta:
        model = Orders
        fields = (
            "first_name",
            "last_name",
            "country",
            "city",
            "address",
            "phone",
            "email",
            "deliver_type",
        )
