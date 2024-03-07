from django.urls import path
from rest_framework import routers

from .views.requestsView import ManageProduct, ProductsLists, RedirectionProductDetail
from .views.requestsCategory import CategoryManagement

urlpatterns = [
    path('products/', ProductsLists.as_view(), name='products-lists'),
    path('product/<int:pk>/',RedirectionProductDetail.as_view(), name='product-detail'),
    path('manage_product/',ManageProduct.as_view(), name='manage-product'),
    path('category/',CategoryManagement.as_view(), name='manage-category'),
]
