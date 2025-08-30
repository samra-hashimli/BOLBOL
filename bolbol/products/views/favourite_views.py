from ..models.favourite import Favourite
from rest_framework import permissions
from rest_framework.views import APIView, Response, status
from ..serializers.favourite_serializer import FavouritesSerializer


class AddToFavouritesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        product_id = request.data.get("product")
        favourite = Favourite.objects.filter(user=user, product_id=product_id)

        if favourite.exists():
            favourite.delete()
            return Response({"message": "Product removed from Favourites"})

        serializer = FavouritesSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"message": "Product added to Favourites successfully"})
        return Response({"errors": serializer.errors}, 
                        status=status.HTTP_400_BAD_REQUEST)