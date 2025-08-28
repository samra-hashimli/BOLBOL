from django.urls import path
from .views import (ProductsAPIView, 
                    ProductDetailAPIView, 
                    CategoriesAPIView,
                    VIPProductsAPIView,
                    PremiumProductsAPIView,
                    AddToFavouritesAPIView,
                    CommentAPIView, 
                    FilteredProductsAPIView)


urlpatterns = [
    path(
        "products/",
        ProductsAPIView.as_view(),
        name="products"
    ),
    path(
        "products/<int:product_id>/",
        ProductDetailAPIView.as_view(),
        name="product-detail"
    ),
    path(
        "categories/",
        CategoriesAPIView.as_view(),
        name="categories"
    ),
    path(
        "products/vip/",
        VIPProductsAPIView.as_view(),
        name="vip-products"
    ),
    path(
        "products/premium/",
        PremiumProductsAPIView.as_view(),
        name="premium-products"
    ),
    path(
        "products/favourites/",
        AddToFavouritesAPIView.as_view(),
        name="fav-products"
    ),
    path(
        "products/<int:product_id>/comments/",
        CommentAPIView.as_view(),
        name="comments"
    ),
    path(
        "products/filter/",
        FilteredProductsAPIView.as_view(),
        name="filtered-products"
    )
]