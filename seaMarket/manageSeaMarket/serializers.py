from rest_framework import serializers
from .models import Product, Category, History

class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True,queryset=Category.objects.all(),source='category_set')
    class Meta:
        model = Product
        fields = ['id','productId','salePrice','price','percentSale','quantity','sellArticle','comments','categories']
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['nameCategory','products']
class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['addDate','typeHistory','valueHistory','products']