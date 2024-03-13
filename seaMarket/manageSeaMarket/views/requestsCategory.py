from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from manageSeaMarket.serializers import CategorySerializer
from manageSeaMarket.models import Category

class CategoryManagement(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        """
        Retrieve all categories and return them as a JSON response.

        Args:
            request: The HTTP request object.
            format: The format of the response data (default is None).

        Returns:
            A JSON response containing all the categories.

        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)
    def post(self,request,format=None):
        try:
            categorySerializer = CategorySerializer(data=request.data)
            if categorySerializer.is_valid():
                category = categorySerializer.save()
                return JsonResponse({'id':category.id}, status=201)
            else:
                return JsonResponse(categorySerializer.errors, status=400)
        except KeyError:
            response = JsonResponse({'error': 'Invalid request data'})
            return HttpResponse(response, status=400)
    def delete(self,request,format=None):
        try:
            category = Category.objects.get(pk=request.data['id'])
            category.delete()
            return JsonResponse({'message':'Category deleted'}, status=200)
        except KeyError:
            response = JsonResponse({'error': 'Invalid request data'})
            return JsonResponse(response, status=400)
    pass