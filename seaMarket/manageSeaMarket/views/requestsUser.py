from django.http import JsonResponse
from manageSeaMarket.models import User
from manageSeaMarket.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser


class UserMangerView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    def put(self, request, format=None):
        user = User.objects.get(pk=request.data['id'])
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    def delete(self, request, format=None):
        user = User.objects.get(pk=request.data['id'])
        if user.has_perm():
            return JsonResponse({'message':'You can not delete an admin'}, status=400)
        user.delete()
        return JsonResponse({'message':'User deleted'}, status=200)