from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.views import View

from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.contenttypes.models import ContentType

from .forms import OrdersForm
from .models import Carts, CartProducts
from .utils import recalc_cart
from accounts.models import Customer


class CartMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.customer = Customer.objects.filter(pk=request.user.pk).first()
            if self.customer:
                self.cart = Carts.objects.filter(Q(owner_id=self.customer.pk) & ~Q(status='in_order')).first()
                if not self.cart:
                    self.cart = Carts.objects.create(owner=self.customer)
                return super(CartMixin, self).dispatch(request, *args, **kwargs)
        messages.error(request, "You have get authorisation first of all!")
        return redirect("user_auth")


class CartView(CartMixin, ListView):
    template_name = "orders/cart.html"
    context_object_name = "cart_products"

    def get_queryset(self):
        return self.cart.cartproducts_set.all()

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context["cart"] = self.cart
        context["order_form"] = OrdersForm()
        return context


class AddCartProductView(CartMixin):
    def get(self, request, **kwargs):
        ct_model, product_pk = kwargs["ct_model"], kwargs["product_pk"]
        ct_object = ContentType.objects.get(model=ct_model)

        product_model = ct_object.model_class()
        product = product_model.objects.get(pk=product_pk)

        cart_product, created = CartProducts.objects.get_or_create(cart=self.cart,
                                                                   product_name=product.title,
                                                                   content_type=ct_object,
                                                                   product_id=product.pk
                                                                   )
        if created:
            cart_product.total_products = 1
            cart_product.total_price = product.price
        else:
            cart_product.total_products += 1
            cart_product.total_price += product.price
        cart_product.save()
        recalc_cart(self.cart)
        return redirect("shop")


class MakeOrder(CartMixin, CreateView):
    form_class = OrdersForm

    def form_valid(self, form):
        order = form.save(commit=False)
        order.cart = self.cart
        order.customer = self.customer
        order.save()

        self.cart.status = "in_order"
        self.cart.save()
        return super(MakeOrder, self).form_valid(form)

    def render_to_response(self, context, **response_kwargs):
        messages.error(self.request, "Ошибка оформления заказа !")
        return redirect("cart")

    def get_success_url(self):
        messages.success(self.request, "Ваш заказ успешно оформлен !")
        return reverse_lazy("home")


