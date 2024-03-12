from django.urls import path
from rest_framework import routers

from manageSeaMarket.views.requestsLogin import LoginView, RefreshTokenView
from manageSeaMarket.views.requestsStats import RevenuesView

from .views.requestsView import ManageHistory, ManageProduct, ProductsLists, RedirectionProductDetail
from .views.requestsCategory import CategoryManagement

urlpatterns = [
    path('products/', ProductsLists.as_view(), name='products-lists'),
    path('product/<int:pk>/',RedirectionProductDetail.as_view(), name='product-detail'),
    path('manage_product/',ManageProduct.as_view(), name='manage-product'),
    path('category/',CategoryManagement.as_view(), name='manage-category'),
    path('login/',LoginView.as_view(), name='login'),
    path('login/refreshtoken/',RefreshTokenView.as_view(), name='refresh-token'),
    path('manage_history/',ManageHistory.as_view(), name='manage-history'),
    path('stats/revenues/',RevenuesView.as_view(), name='stats'),
]
