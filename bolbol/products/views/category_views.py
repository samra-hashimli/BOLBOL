from ..models.category import Category
from rest_framework.views import APIView, Response
from ..serializers.category_serializer import CategorySerializer


class CategoriesAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)