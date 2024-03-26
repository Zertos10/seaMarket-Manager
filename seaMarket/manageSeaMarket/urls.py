from django.urls import path
from rest_framework import routers

from manageSeaMarket.views.requestsLogin import LoginView, RefreshTokenView
from manageSeaMarket.views.requestsStats import AccountingView, MarginView, RevenuesView
from manageSeaMarket.views.requestsUser import UserMangerView

from .views.requestsView import ManageHistory, ManageProduct, ProductsLists, RedirectionProductDetail, RedirectionProducts
from .views.requestsCategory import CategoryManagement

urlpatterns = [
    path('', ProductsLists.as_view(), name='products-lists'),
    #Products
    path('products/', ProductsLists.as_view(), name='products-lists'),
    path('products/<int:pk>/', ProductsLists.as_view(), name='products-lists'),

    path('product/<int:pk>/',RedirectionProductDetail.as_view(), name='product-detail'),
    path('products/redirection/',RedirectionProducts.as_view(), name='products-redirection'),
    path('manage_product/',ManageProduct.as_view(), name='manage-product'),
    path('category/',CategoryManagement.as_view(), name='manage-category'),
    #Authentification
    path('login/',LoginView.as_view(), name='login'),
    path('login/refreshtoken/',RefreshTokenView.as_view(), name='refresh-token'),
    #Stats
    path('manage_history/',ManageHistory.as_view(), name='manage-history'),
    path('stats/revenues/',RevenuesView.as_view(), name='stats'),
    path('stats/margin/',MarginView.as_view(), name='margin'),
    path('accounting/',AccountingView.as_view(), name='accounting'),
    #User
    path('manage_user/',UserMangerView.as_view(), name='manage-user')
]
