import json

from django.db.models import F
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.views import APIView, Response, status
from ..models.product import Product
from ..models.category import Category
from ..models.subcategory import SubCategory
from ..serializers.product_serializer import ProductSerializer


class ProductsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        category_id = request.query_params.get("category")
        city_id = request.query_params.get("city")
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")

        if city_id:
            products = products.filter(city_id=city_id)

        if category_id:
            products = products.filter(category_id=category_id)

        if min_price:
            products = products.filter(price__gt=min_price)

        if max_price:
            products = products.filter(price__lt=max_price)

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
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class VIPProductsAPIView(APIView):
    def get(self, request):
        vip_products = Product.objects.filter(
            subscriptions__subscription_type__subscription_name="VIP",
            subscriptions__activated_at__lte=timezone.now(),
            subscriptions__expires_at__gt=timezone.now(),
        ).distinct()

        serializer = ProductSerializer(vip_products, many=True)
        return Response(serializer.data)


class PremiumProductsAPIView(APIView):
    def get(self, request):
        premium_products = Product.objects.filter(
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
        product = get_object_or_404(Product, id=product_id)

        product.views_count = F("views_count") + 1
        product.save(update_fields=["views_count"])
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
        product = get_object_or_404(Product, id=product_id)

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
        product = get_object_or_404(Product, id=product_id)

        if product.user != request.user:
            return Response({"message": "Not allowed"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)


class ProductParametersAPIView(APIView):
    def get(self, request, category_id, subcategory_id):
        with open(settings.BASE_DIR / "parameters.json", "r") as f:
            parameters = json.load(f)

        category = get_object_or_404(Category, id=category_id)
        subcategory = get_object_or_404(SubCategory, id=subcategory_id)

        try:
            fields = parameters[category.name][subcategory.name]
        except KeyError:
            fields = []

        return Response({"fields": fields})
