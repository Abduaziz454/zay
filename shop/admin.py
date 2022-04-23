from django.contrib import admin

from . import models
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

# admin.site.register(Address)
@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("pk", "title")
    list_display_links = ("pk", "title")


class ProductModelChildren(PolymorphicChildModelAdmin):
    base_model = models.Product

@admin.register(models.MenClothes)
class MenClothesAdmin(ProductModelChildren):
    list_display = ("pk", "title", "brand", "image", "size", "is_published")
    list_display_links = ("title", )
    list_editable = ("image", "is_published")

@admin.register(models.WomenClothes)
class WomenClothesAdmin(ProductModelChildren):
    list_display = ("pk", "title", "image", "size", "is_published")
    list_display_links = ("title", )
    list_editable = ("image", "is_published")

@admin.register(models.Gadgets)
class GadgetsAdmin(ProductModelChildren):
    list_display = ("pk", "title", "company")
    list_display_links = ("title", )


@admin.register(models.Product)
class ProductAdmin(PolymorphicParentModelAdmin):
    base_model = models.Product
    child_models = [models.MenClothes, models.WomenClothes, models.Gadgets]

@admin.register(models.Followers)
class FollowersAdmin(admin.ModelAdmin):
    list_display = ("pk", "email")
    list_display_links = ("email",)
    search_fields = ("email",)
    ordering = ("pk",)

@admin.register(models.ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ("product", "image")


@admin.register(models.ProductReviews)
class ProductReviewsAdmin(admin.ModelAdmin):
    list_display = ("author", "product")

@admin.register(models.Mail_Contacts)
class MessagesView(admin.ModelAdmin):
    list_display = ("name", "email")

