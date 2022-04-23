from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("shop/", views.ShopPageView.as_view(), name="shop"),
    path("contact/", views.ContactPageView.as_view(), name="contact"),
    path("contact/", views.AddressView.as_view(), name="contact"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path("add-followers/", views.FollowerCreateView.as_view(), name="add_follower"),
    path("send-message/", views.SendMessage.as_view(), name="send_message"),
    path("category/<str:slug>/", views.CategoriesPage.as_view(), name="categories_page"),
    path("product/<str:slug>/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),

]