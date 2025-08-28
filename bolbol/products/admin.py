from django.contrib import admin
from django.utils import timezone
from .models import (
    City, Brand, Category, SubCategory, 
    Product, Favourite, Comment, ProductImage,
    Subscription, ProductSubscription
)

# ---------------- City Admin ----------------
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# ---------------- Brand Admin ----------------
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# ---------------- Category & SubCategory Admin ----------------
class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    inlines = [SubCategoryInline]

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')


# ---------------- Product & ProductImage Admin ----------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'price', 'status', 'vip_status', 'premium_status',
        'views_count', 'created_at', 'expires_at'
    )
    list_filter = ('status', 'category', 'subcategory', 'created_at')
    search_fields = ('title', 'description', 'user__phone_number')
    readonly_fields = ('views_count', 'created_at', 'updated_at', 'expires_at')
    inlines = [ProductImageInline]
    list_editable = ('status',)

    def vip_status(self, obj):
        return obj.subscriptions.filter(
            subscription_type__subscription_name="VIP",
            expires_at__gt=timezone.now()
        ).exists()
    vip_status.boolean = True
    vip_status.short_description = "VIP"

    def premium_status(self, obj):
        return obj.subscriptions.filter(
            subscription_type__subscription_name="Premium",
            expires_at__gt=timezone.now()
        ).exists()
    premium_status.boolean = True
    premium_status.short_description = "Premium"


# ---------------- Subscription & ProductSubscription Admin ----------------
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscription_name', 'price', 'availability_time')
    search_fields = ('subscription_name',)


@admin.register(ProductSubscription)
class ProductSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'subscription_type', 'activated_at', 'expires_at', 'is_active')
    list_filter = ('subscription_type',)
    search_fields = ('product__title', 'subscription_type__subscription_name')
    readonly_fields = ('activated_at', 'expires_at')

    def is_active(self, obj):
        return obj.is_active()
    is_active.boolean = True
    is_active.short_description = "Active"


# ---------------- Favourites Admin ----------------
@admin.register(Favourite)
class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'bookmarked_at')
    list_filter = ('bookmarked_at',)
    search_fields = ('user__phone_number', 'product__title')
    ordering = ('-bookmarked_at',)
    readonly_fields = ('bookmarked_at',)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)


# ---------------- Comment Admin ----------------
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'short_text', 'created_at')
    list_filter = ('created_at', 'product')
    search_fields = ('text', 'user__phone_number', 'product__title')
    readonly_fields = ('created_at',)

    def short_text(self, obj):
        return obj.text[:40] + "..." if len(obj.text) > 40 else obj.text
    short_text.short_description = "Comment"
