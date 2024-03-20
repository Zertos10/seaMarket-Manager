import datetime
from http.client import responses
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.forms.models import model_to_dict
import requests
from manageSeaMarket.models import Category, History, Product
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
            requestProduct = requests.get(url=URL_PRODUCT + "product/" + str(produit.productId) + "/")
            data = serializedProduct.data
            data['name'] = requestProduct.json()['name']
            res.append(data)
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
            if createData.get('categories'):
                categories = createData.pop('categories')
            serializedProduct = ProductSerializer(data=request.data)
            print(serializedProduct.required)
            if serializedProduct.is_valid():
                product =serializedProduct.save()
                if categories:
                    for category in categories:
                        categoryObject = Category.objects.get(id=category)
                        categoryObject.products.add(product)
                        categoryObject.save()
                print(product)
                HistoryManagement(createData,product).createProduct()
                return JsonResponse(serializedProduct.data,status=201)
            else :
                print(serializedProduct.error_messages)
                return JsonResponse(serializedProduct.errors, status=400)
        except KeyError as e:
            print("exception"+e.__str__())
            return HttpResponse(status=400, content=e.__str__())
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
                    return JsonResponse({'error':'Product does not exist'+ product,'success':'product'}, status=400)
            return JsonResponse({'message':'Products deleted','ids': products }, status=200)   
        except KeyError:
            # Handle KeyError exception
            responses = 'Bad Request : The request data is invalid.'
            return JsonResponse({'error':responses}, status=400)
    def patch(self, request, format=None):
        try:
            productDoesntExist = []
            data = request.data
            responseProductUpdated= []
            for product in data:
                try:
                    productToUpdate = Product.objects.get(id=int(product['id']))
                    
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
                            responseProductUpdated.append(JsonResponse(serializedProduct.data,status=200))
                        else: 
                            responseProductUpdated.append(JsonResponse([{"error":serializedProduct.error_messages,"id":product}], status=400))
                    
                except Product.DoesNotExist:
                    responseProductUpdated.append(JsonResponse({'error':'Product does not exist','id':product}, status=400))
        except KeyError:
            # Handle KeyError exception
            responses = 'Bad Request : The request data is invalid.'
            return HttpResponse(status=400, content=responses)
        return JsonResponse(responseProductUpdated, safe=False,status=200)
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
