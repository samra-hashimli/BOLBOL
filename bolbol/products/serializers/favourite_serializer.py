from rest_framework.serializers import ModelSerializer
from ..models.favourite import Favourite


class FavouritesSerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = "__all__"
