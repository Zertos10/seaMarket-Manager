from tokenize import TokenError
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    def post(self, request, format=None):
        requestJson = request.data
        email = requestJson['email']
        password = requestJson['password']
        user = authenticate(email=email, password=password)
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
class RefreshTokenView(APIView):
    def post(self, request, format=None):
        refreshToken = request.data['refresh']
        try:
            token = RefreshToken(refreshToken)
            return JsonResponse({'access':str(token.access_token)},status=200)
        except TokenError:
            return HttpResponse(status=401)