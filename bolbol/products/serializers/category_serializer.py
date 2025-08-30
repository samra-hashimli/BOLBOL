from rest_framework.serializers import ModelSerializer
from ..models.category import Category
from .subcategory_serializer import SubCategorySerializer


class CategorySerializer(ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "subcategories"]
