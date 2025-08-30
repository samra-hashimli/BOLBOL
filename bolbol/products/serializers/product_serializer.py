import json

from django.conf import settings
from ..models.product import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def validate_characteristics(self, value):
        category = self.initial_data.get("category")
        subcategory = self.initial_data.get("subcategory")

        if category and subcategory:
            from ..models import Category, SubCategory
            ctg = Category.objects.get(id=category)
            sub = SubCategory.objects.get(id=subcategory)

            with open(settings.BASE_DIR / "parameters.json", "r") as f:
                parameters = json.load(f)

            valid_fields = parameters.get(ctg.name, {}).get(sub.name, [])

            for key in value.keys():
                if key not in valid_fields:
                    raise serializers.ValidationError(
                        f"'{key}' is not a valid field for {ctg.name} -> {sub.name}"
                    )

        return value
