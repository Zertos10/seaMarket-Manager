from tokenize import TokenError
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth import models

from manageSeaMarket.models import User


class LoginView(APIView):
    def post(self, request, format=None):
        requestJson = request.data
        email = requestJson['email']
        password = requestJson['password'] 
        result =self.check_hash(email, password)
        user = None
        if result is None:
            user = authenticate(email=email, password=password)
        else:
            user = result
        if user is not None:
            refreshToken = RefreshToken.for_user(user)
            print(refreshToken)
            print(refreshToken.access_token)
            return JsonResponse({'refresh': str(refreshToken),
                                 'access':str(refreshToken.access_token),
                                 "refresh_exp":str(refreshToken.lifetime),
                                 "access_exp":str(refreshToken.access_token.lifetime),
                                 },status=200)
        else:
            return HttpResponse(status=401)
    pass
    def check_hash(self, email, hashed_password):
        try:
            user = User.objects.get(email=email)
        except models.User.DoesNotExist:
            return None

        if check_password(hashed_password, user.password):
            return user

        return None
class RefreshTokenView(APIView):
    def post(self, request, format=None):
        refreshToken = request.data['refresh']
        try:
            token = RefreshToken(refreshToken)
            return JsonResponse({'access':str(token.access_token)},status=200)
        except TokenError:
            return HttpResponse(status=401)