from rest_framework.serializers import ModelSerializer
from .models import (Product, Category, 
                     SubCategory, Favourite,
                     Comment)


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class SubCategorySerializer(ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"


class CategorySerializer(ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "subcategories"]


class FavouritesSerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = "__all__"


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"