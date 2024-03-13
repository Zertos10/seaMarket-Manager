from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from manageSeaMarket.services.servicesCA import AccountingResult, MarginCalculation, RevenuesCalculation

class RevenuesView(APIView):
    #permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        data_params = request.query_params
        if data_params.get('type') and data_params.get('category'):
            service = RevenuesCalculation(category=data_params.get('category'), typeDate=data_params.get('type'), 
                                             maxDate= data_params.get('maxDate') if data_params.get('maxDate') else None, 
                                             minDate=data_params.get('minDate') if data_params.get('maxDate') else None)
            return HttpResponse(service.calculate(),status=200)
        else:
            return HttpResponse(status=400) 
    pass
class MarginView(APIView):
    def get(self,request,format=None):
        data_params = request.query_params
        if data_params.get('category'):
            service = MarginCalculation(category=data_params.get('category'),
                                        typeDate=data_params.get('type'),
                                        maxDate= data_params.get('maxDate') if data_params.get('maxDate') else None, 
                                        minDate=data_params.get('minDate') if data_params.get('maxDate') else None)
            return HttpResponse(service.calculate(),status=200)
        else:
            return HttpResponse(status=400)
class AccountingView(APIView):
    def get(self,request,format=None):
        service = AccountingResult()
        return JsonResponse({'tax':service()},status=200)
    pass
