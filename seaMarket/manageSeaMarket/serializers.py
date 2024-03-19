from rest_framework import serializers
from .models import Product, Category, History, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','lastName','firstName','isAdmin']

class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True,queryset=Category.objects.all(),source='category_set',required=False)
    class Meta:
        model = Product
        fields = ['id','productId','salePrice','price','percentSale','quantity','sellArticle','comments','categories']
class CategorySerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(required=False,many=True,queryset=Product.objects.all(),source='product_set')
    class Meta:
        model = Category
        fields = ['id','nameCategory','products']
class HistorySerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model = History
        fields = ['addDate','typeHistory','quantityHistory','valueHistory','product']