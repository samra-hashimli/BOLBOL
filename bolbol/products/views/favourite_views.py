from django.shortcuts import get_object_or_404
from ..models.favourite import Favourite
from ..models.product import Product
from rest_framework import permissions
from rest_framework.views import APIView, Response, status
from ..serializers.favourite_serializer import FavouritesSerializer


class AddToFavouritesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        product_id = request.data.get("product")

        product = get_object_or_404(Product, id=product_id)  

        favourite = Favourite.objects.filter(user=user, product=product)

        if favourite.exists():
            favourite.delete()
            return Response({"message": "Product removed from Favourites"})

        serializer = FavouritesSerializer(data={"product": product.id})
        if serializer.is_valid():
            serializer.save(user=user, product=product)
            return Response({"message": "Product added to Favourites successfully"})
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
