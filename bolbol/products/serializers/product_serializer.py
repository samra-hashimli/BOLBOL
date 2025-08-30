from rest_framework.serializers import ModelSerializer
from ..models.product import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
