from django.db import models
from .category import Category


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
