from rest_framework.serializers import ModelSerializer
from ..models.subcategory import SubCategory


class SubCategorySerializer(ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"