from django.db import models
from accounts.models.user import User
from accounts.utils.masking import mask_fullname
from .product import Product


class Comment(models.Model):
    text = models.TextField(max_length=350)
    product = models.ForeignKey(Product, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user.full_name:
            masked_name = mask_fullname(self.user.full_name) or self.user.phone_number
            return f"{masked_name} - {self.product.title}"
        return f"{self.user.phone_number} - {self.product.title}"
