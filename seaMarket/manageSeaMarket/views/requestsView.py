import datetime
from http.client import responses
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.forms.models import model_to_dict
import requests
from manageSeaMarket.models import History, Product
from manageSeaMarket.serializers import  HistorySerializer, ProductSerializer
from manageSeaMarket.services.servicesCA import HistoryManagement
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
            res.append(serializedProduct.data)
            print(res)
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
            print(createData)
            if serializedProduct.is_valid():
                product =serializedProduct.save()
                
                createData['reason'] = 'create'
                print(product)
                HistoryManagement(createData,product).createProduct()
                return HttpResponse(status=201)
            else :
                return HttpResponse(status=400, content='Bad Request: The request data is invalid.'+" "+str(serializedProduct.errors))
        except KeyError as e:
            # Handle KeyError exception
            responses = 'Bad Request : The request data is invalid.'+" "+str(e.__str__())
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
                    Product.objects.get(productId=int(product)).delete()
                except Product.DoesNotExist: 
                    return HttpResponse(status=404,content='Not Found: The product does not exist.(' + str(product) + ')')
            return HttpResponse(status=200, content='OK: This product has been deleted.(' + str(products) + ')')   
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
                    
                    if product.get('price') and product.get('quantity') and product.get('reason'):
                        historyManagement =HistoryManagement(product,productToUpdate)
                        if product.get('reason') == 'sell' or product.get('reason') == 'unsold':
                            return historyManagement.sellProduct()
                        elif product.get('reason') == 'buy':
                            return historyManagement.addProduct()
                    else :
                        if product.get('reason'):
                            product.pop('reason')
                        serializedProduct = ProductSerializer(productToUpdate, data=product, partial=True)
                        if serializedProduct.is_valid():
                            serializedProduct.save()
                            return JsonResponse(serializedProduct.data,status=200)
                        else: 
                            return JsonResponse(serializedProduct.error_messages, status=400)
                    
                except Product.DoesNotExist:
                    productDoesntExist.append(product['productId'])
        except KeyError:
            # Handle KeyError exception
            responses = 'Bad Request : The request data is invalid.'
            return HttpResponse(status=400, content=responses)
    pass
class ManageHistory(APIView):
    def get(self, request, format=None):
        """
        Retrieve all history and return them as a JSON response.

        Args:
            request: The HTTP request object.
            format: The format of the response data (default is None).

        Returns:
            A JSON response containing all the history.

        """
        res = []
        for history in History.objects.all():
            serializedHistory = HistorySerializer(history)
            res.append(serializedHistory.data)
        return JsonResponse(res, safe=False)
    pass
