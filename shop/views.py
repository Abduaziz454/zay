from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from orders.views import CartMixin
from . import models
from .models import Address

class HomePage(CartMixin, ListView):
    template_name = "shop/index.html"
    context_object_name = "products"

    def get_queryset(self):
        return models.Product.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context["recommends_products"] = models.Product.objects.filter(
            is_published=True
        ).order_by("-count_views")[:4]
        context["cart"] = self.cart
        return context



class ShopPageView(CartMixin, ListView):
    template_name = "shop/shop.html"
    context_object_name = "products"

    def get_queryset(self):
        return models.Product.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super(ShopPageView, self).get_context_data(**kwargs)
        context["mens_clothes"] = models.MenClothes.objects.filter(
            is_published=True,
        ).order_by("-time_update")
        context["womens_clothes"] = models.WomenClothes.objects.filter(
            is_published=True,
        ).order_by("-time_update")
        context["gadgets"] = models.Gadgets.objects.filter(
            is_published=True,
        ).order_by("-time_update")
        context["cart"] = self.cart
        return context

class ContactPageView(CartMixin, ListView):
    template_name = "shop/contact.html"
    context_object_name = "contact"

    def get_queryset(self):
        return

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ContactPageView, self).get_context_data(**kwargs)
        context["cart"] = self.cart
        return context

class AddressView(CreateView):

    model = Address
    fields = ['address']
    template_name = 'shop/contact.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mapbox_access_token'] = 'pk.eyJ1IjoiYWJkdWF6aXoiLCJhIjoiY2t6bnFtZmxoMDljYzJ2cWdqOXc5NHJtMSJ9.2bquCt0JhPU3o3FYSPP8Hw'
        context['addresses'] = Address.objects.all()
        return context

class AboutPageView(CartMixin, ListView):
    template_name = "shop/about.html"
    context_object_name = "about"

    def get_queryset(self):
        return

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AboutPageView, self).get_context_data(**kwargs)
        context["cart"] = self.cart
        return context

class FollowerCreateView(CreateView):
    model = models.Followers
    fields = ("email", )


    def render_to_response(self, context, **response_kwargs):
        messages.error(self.request, "User with that email exists")
        return redirect("home")

    def get_success_url(self):
        messages.success(self.request, f"Your email {self.object.email} has been added !")
        return reverse_lazy("home")

class SendMessage(CreateView):
    model = models.Mail_Contacts
    fields = ("email", "name", "subject", "message")


    def render_to_response(self, context, **response_kwargs):
        messages.error(self.request, "Message has not been sent !")
        return redirect("home")

    def get_success_url(self):
        messages.success(self.request, f"Your email message has been sent !")
        return reverse_lazy("home")

class CategoriesPage(ListView):
    template_name = "shop/category_detail.html"
    context_object_name = "products"

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs["slug"]
        ct_object = ContentType.objects.get(model=slug)
        self.model = ct_object.model_class()
        return super(CategoriesPage, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(is_published=True)

class ProductDetailView(CartMixin, DetailView):
    template_name = "shop/shop-single.html"
    context_object_name = "product"

    def dispatch(self, request, *args, **kwargs):
        # Получение модели продукта
        slug = self.kwargs["slug"]
        ct_object = ContentType.objects.get(model=slug)
        self.model = ct_object.model_class()

        # Увеличиваем просмотры у товара
        product = self.get_object()
        product.count_views += 1
        product.save()

        return super(ProductDetailView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context["slider_images"] = models.ProductImages.objects.filter(product_id=self.kwargs["pk"])
        context["recommends_products"] = self.model.objects.filter(
            is_published=True
        ).order_by("-count_views")[:4]
        context["cart"] = self.cart

        return context
