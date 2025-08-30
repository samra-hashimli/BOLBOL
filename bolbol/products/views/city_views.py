from ..models.city import City
from rest_framework.views import APIView, Response
from ..serializers.city_serializer import CitySerializer


class CitiesAPIView(APIView):
    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)