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
class RequestProductSerializer(serializers.Serializer):
    availability = serializers.BooleanField()
    name = serializers.CharField()
    commentProduct = serializers.CharField(source='comments')
    owner = serializers.CharField()
    discount = serializers.DecimalField(max_digits=5, decimal_places=2)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    unit = serializers.IntegerField()
    sale = serializers.BooleanField()