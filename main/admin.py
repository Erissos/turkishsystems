from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from .models import (
    NavLink,
    PortfolioItem,
    PricingPackage,
    Product,
    ProductFAQ,
    ProductOrder,
    ProductPackage,
    ProductReview,
    Service,
    SiteSettings,
    SocialLink,
    Stat,
)

@admin.register(PricingPackage)
class PricingPackageAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_highlighted", "order")
    list_editable = ("order", "is_highlighted")



@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("brand_name", "meta_title")


@admin.register(NavLink)
class NavLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "url", "is_primary", "order")
    list_editable = ("order", "is_primary")


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "color_class", "order")
    list_editable = ("order",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "accent_class", "order")
    list_editable = ("order",)


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ("title", "image", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "url", "order")
    list_editable = ("order",)


class ProductPackageInline(admin.TabularInline):
    model = ProductPackage
    extra = 0
    fields = ("name", "price", "is_highlighted", "ask_details_on_order", "order")


class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 0
    fields = ("full_name", "role", "is_published", "order")


class ProductFAQInline(admin.TabularInline):
    model = ProductFAQ
    extra = 0
    fields = ("question", "is_active", "order")


class ProductOrderInline(admin.TabularInline):
    model = ProductOrder
    extra = 0
    can_delete = False
    fields = ("package", "full_name", "email", "phone", "detail_note", "created_at")
    readonly_fields = ("package", "full_name", "email", "phone", "detail_note", "created_at")


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "order")
    list_editable = ("is_active", "order")
    prepopulated_fields = {"slug": ("name",)}
    inlines = (ProductPackageInline, ProductReviewInline, ProductFAQInline, ProductOrderInline)


try:
    admin.site.register(Product, ProductAdmin)
except AlreadyRegistered:
    admin.site.unregister(Product)
    admin.site.register(Product, ProductAdmin)
