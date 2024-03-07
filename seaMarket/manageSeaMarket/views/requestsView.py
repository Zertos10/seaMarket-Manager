from http.client import responses
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import requests
from manageSeaMarket.models import Product
from manageSeaMarket.serializers import  ProductSerializer
from seaMarket.settings import URL_PRODUCT

# Create your views here.
class ProductsLists(APIView):
    """
    A view for retrieving product lists.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        """
        Retrieve all products and return them as a JSON response.

        Args:
            request: The HTTP request object.
            format: The format of the response data (default is None).

        Returns:
            A JSON response containing all the products.

        """
        res = []
        print(Product.objects.count())
        for produit in Product.objects.all():
            serializedProduct = ProductSerializer(produit)
            print(serializedProduct.data)
            res.append(serializedProduct.data)
        return JsonResponse(res, safe=False)
    pass
class RedirectionProductDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        """
        Retrieve details of a product and return serialized data.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the product to retrieve.
            format (str, optional): The format of the response data. Defaults to None.

        Returns:
            JsonResponse: The serialized product detail data.

        Raises:
            HttpResponse: If the product does not exist.
            HttpResponse: If the request data is invalid.
        """

        try:
            product = Product.objects.get(pk=pk)
            requestProduct = requests.get(url=URL_PRODUCT + "product/" + str(pk) + "/")
            productSerializer =ProductSerializer(product)
            requestJson = requestProduct.json()
            requestJson['commentProduct'] = requestJson.pop('comments')
            requestJson.update(productSerializer.data)
            return JsonResponse(requestJson, safe=False)
        except Product.DoesNotExist:
            return HttpResponse(status=404)
        except KeyError:
            return HttpResponse(status=400, content='Bad Request: The request data is invalid.')
class ManageProduct(APIView):
    """
    A view for managing products.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        
        try:
            createData =request.data
            serializedProduct = ProductSerializer(data=createData)
            
            if serializedProduct.is_valid():
                product =serializedProduct.save()
                return HttpResponse({'id': product.id},status=201)
            else :
                return HttpResponse(status=400, content='Bad Request: The request data is invalid.')
        except KeyError:
            # Handle KeyError exception
            responses = 'Bad Request : The request data is invalid.'
            return HttpResponse(status=400, content=responses)
    def delete(self, request, format=None):
        """
        Permet de supprimer un ou plusieurs produits.

        Args:
            request (HttpRequest): L'objet HttpRequest contenant les données de la requête.
            format (str, optional): Le format de la réponse. Par défaut, None.

        Returns:
            HttpResponse: L'objet HttpResponse contenant la réponse de la requête.

        Raises:
            KeyError: Si la clé 'ids' est absente dans les données de la requête.
            Product.DoesNotExist: Si un produit avec l'identifiant spécifié n'existe pas.
        """
        try:
            products = request.data['ids']
            for product in products:
                try:
                    Product.objects.get(productId=product).delete()
                except Product.DoesNotExist: 
                    return HttpResponse(status=404,content='Not Found: The product does not exist.(' + str(product) + ')')
            return HttpResponse(status=200, content='OK: This product has been deleted.(' + str(products) + ')')   
        except KeyError:
            # Handle KeyError exception
            responses = 'Bad Request : The request data is invalid.'
            return HttpResponse(status=400, content=responses)
    def put(self, request, format=None):
        try:
            productDoesntExist = []
            data = request.data
            for product in data:
                try:
                    productToUpdate = Product.objects.get(id=product['id'])
                    serializedProduct = ProductSerializer(productToUpdate, data=product)
                    Product.save(serializedProduct)
                except Product.DoesNotExist:
                    productDoesntExist.append(product['productId'])
        except KeyError:
            # Handle KeyError exception
            responses = 'Bad Request : The request data is invalid.'
            return HttpResponse(status=400, content=responses)
    def patch(self, request, format=None):
        try:
            productDoesntExist = []
            data = request.data
            for product in data:
                try:
                    productToUpdate = Product.objects.get(id=product['id'])
                    serializedProduct = ProductSerializer(productToUpdate, data=product, partial=True)
                    Product.save(serializedProduct)
                except Product.DoesNotExist:
                    productDoesntExist.append(product['productId'])
        except KeyError:
            # Handle KeyError exception
            responses = 'Bad Request : The request data is invalid.'
            return HttpResponse(status=400, content=responses)
    pass