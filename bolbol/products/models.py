from datetime import timedelta
from django.utils import timezone
from django.db import models
from accounts.utils.masking import mask_fullname
from accounts.models.user import User


class City(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class SubCategory(models.Model):
    name = models.CharField(max_length=32, unique=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name="subcategories"
    )

    def __str__(self):
        return f"{self.category.name} -> {self.name}"
    
    class Meta:
        verbose_name = "Sub-category"
        verbose_name_plural = "Sub-categories"


class Product(models.Model):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"

    STATUS_LIST = [
        (PENDING, "PENDING"),
        (APPROVED, "APPROVED"),
        (REJECTED, "REJECTED"),
        (EXPIRED, "EXPIRED"),
    ]

    title = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=500)
    views_count = models.PositiveIntegerField(default=0)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    subcategory = models.ForeignKey(
        SubCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    city = models.ForeignKey(
        City, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    status = models.CharField(
        choices=STATUS_LIST,
        default=PENDING,
        max_length=16
    )
    is_vip = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    is_new = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    delivery_available = models.BooleanField(default=False)
    credit_available = models.BooleanField(default=False)
    barter_available = models.BooleanField(default=False)
    # image = models.ImageField(upload_to="products/", null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.status})"

    def save(self, *args, **kwargs):
        if self.status == self.APPROVED and not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=30)

        if self.expires_at and self.expires_at < timezone.now():
            self.status = self.EXPIRED

        super().save(*args, **kwargs)

        if self.is_vip:
            subscription, _ = Subscription.objects.get_or_create(
                subscription_name="VIP",
                defaults={"price": 0, "availability_time": timedelta(days=30)}
            )
            ProductSubscription.objects.get_or_create(
                product=self,
                subscription_type=subscription,
                defaults={
                    "expires_at": timezone.now() + subscription.availability_time
                }
            )
        else:
            ProductSubscription.objects.filter(
                product=self,
                subscription_type__subscription_name="VIP"
            ).delete()

        if self.is_premium:
            subscription, _ = Subscription.objects.get_or_create(
                subscription_name="Premium",
                defaults={"price": 0, "availability_time": timedelta(days=30)}
            )
            ProductSubscription.objects.get_or_create(
                product=self,
                subscription_type=subscription,
                defaults={
                    "expires_at": timezone.now() + subscription.availability_time
                }
            )
        else:
            ProductSubscription.objects.filter(
                product=self,
                subscription_type__subscription_name="Premium"
            ).delete()

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    bookmarked_at = models.DateTimeField(auto_now_add=True,
                                         null=True,
                                         blank=True)

    def __str__(self):
        return f"{self.user} liked {self.product}"
    

class Comment(models.Model):
    text = models.TextField(max_length=350)
    product = models.ForeignKey(
        Product, 
        related_name="comments", 
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user.full_name:
            masked_name = mask_fullname(self.user.full_name) or self.user.phone_number
            return f"{masked_name} - {self.product.title}"
        return f"{self.user.phone_number} - {self.product.title}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name="images"
    )
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return self.product.title


class Subscription(models.Model):
    subscription_name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    availability_time = models.DurationField()
    
    def __str__(self):
        return self.subscription_name


class ProductSubscription(models.Model):
    product = models.ForeignKey(
        "Product", 
        on_delete=models.CASCADE, 
        related_name="subscriptions"
    )
    subscription_type = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    activated_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + self.subscription_type.availability_time
        return super().save(*args, **kwargs)
    
    def is_active(self):
        return self.expires_at > timezone.now()

    def __str__(self):
        return f"{self.product.title} -> {self.subscription_type.subscription_name}"