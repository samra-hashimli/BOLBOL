from django.utils import timezone
from rest_framework import permissions
from rest_framework.views import APIView, Response, status
from ..models.product import Product
from django.db.models import F
from ..serializers.product_serializer import ProductSerializer


class ProductsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        products = Product.objects.filter(
            status=Product.APPROVED,
            expires_at__gt=timezone.now()
        )
        category_id = request.query_params.get("category")
        city_id = request.query_params.get("city")

        if city_id:
            products = products.filter(city_id=city_id)

        if category_id:
            products = products.filter(category_id=category_id)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": "New product created"},
                status=status.HTTP_201_CREATED
            )
        return Response({"errors": serializer.errors}, status=400)
    

class VIPProductsAPIView(APIView):
    def get(self, request):
        vip_products = Product.objects.filter(
            status=Product.APPROVED,
            subscriptions__subscription_type__subscription_name="VIP",
            subscriptions__activated_at__lte=timezone.now(),
            subscriptions__expires_at__gt=timezone.now(),
        ).distinct()

        serializer = ProductSerializer(vip_products, many=True)
        return Response(serializer.data)


class PremiumProductsAPIView(APIView):
    def get(self, request):
        premium_products = Product.objects.filter(
            status=Product.APPROVED,
            subscriptions__subscription_type__subscription_name="Premium",
            subscriptions__activated_at__lte=timezone.now(),
            subscriptions__expires_at__gt=timezone.now(),
        ).distinct()

        serializer = ProductSerializer(premium_products, many=True)
        return Response(serializer.data)
    

class FilteredProductsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        status_param = request.query_params.get("status")
        subscription_param = request.query_params.get("subscription")

        if status_param:
            products = products.filter(status=status_param)

        if subscription_param:
            now = timezone.now()
            products = products.filter(
                subscriptions__subscription_type__subscription_name=subscription_param,
                subscriptions__activated_at__lte=now,
                subscriptions__expires_at__gt=now,
            ).distinct()

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailAPIView(APIView):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        product.view_count = F("views_count" + 1)
        product.save(update_fields=["view_count"])
        product.refresh_from_db()

        serializer = ProductSerializer(product)

        similar_products = Product.objects.filter(
            category=product.category,
            status=Product.APPROVED,
            expires_at__gt=timezone.now()
        ).exclude(id=product.id)

        similar_products_serializer = ProductSerializer(similar_products, many=True)

        return Response({
            "product": serializer.data,
            "similar_products": similar_products_serializer.data
        })

    def put(self, request, product_id):
        product = Product.objects.get(id=product_id)

        if product.user != request.user:
            return Response({"message": "Not allowed"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product updated successfully"})
        
        return Response({"errors": serializer.errors}, 
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = Product.objects.get(id=product_id)

        if product.user != request.user:
            return Response({"message": "Not allowed"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        product.delete()
        return Response({"message": "Product deleted successfully"}, 
                        status=status.HTTP_200_OK)
