from django.http import JsonResponse
from manageSeaMarket.models import History, Product
import pandas as pd
import numpy as np
import datetime

from manageSeaMarket.serializers import HistorySerializer, ProductSerializer


class RevenuesCalculation():
    """Calcule le chiffre d'affaire d'une catégorie de produit sur une période donnée.
    """
    typeHistory = 'sell'
    def __init__(self, category, typeDate:str,maxDate=None,minDate=None):
        self.category = category
        self.typeDate = typeDate
        self.maxDate = maxDate
        self.minDate = minDate
        self.convertDate()
    def convertDate(self):
        if self.maxDate is not None:
            self.maxDate = datetime.datetime.strptime(self.maxDate, '%Y-%m-%dT%H:%M:%S.%fZ')
        if self.minDate is not None:
            self.minDate = datetime.datetime.strptime(self.minDate, '%Y-%m-%dT%H:%M:%S.%fZ')
    def convertTypeDate(self):
        if self.typeDate == 'day':
            typeDate = 'D'
        elif self.typeDate == 'week':
            typeDate = 'W'
        elif self.typeDate == 'month':
            typeDate = 'M'
        elif self.typeDate == 'year':
            typeDate = 'Y'
        else :
            typeDate = 'W'
        return typeDate
    def calculateTurnover(self):

        if self.minDate is None:
            self.minDate = datetime.datetime.now()
            print(self.minDate)
        result = None
        if self.maxDate is None:
            result = History.objects.filter(typeHistory=self.typeHistory, product__category__id= self.category if self.category is not None else 1)
        else:
            result = History.objects.filter(addDate__range=[self.maxDate,self.minDate], typeHistory=self.typeHistory, products__category=self.category)
        historySerializer = HistorySerializer(result, many=True)
        print(result)
        df = pd.DataFrame({
            "date": [history['addDate'] for history in historySerializer.data],
            "value": [history['valueHistory'] for history in historySerializer.data],
            "quantity": [history['quantityHistory'] for history in historySerializer.data]
        })
        df['date'] = pd.to_datetime(df['date']) - pd.Timedelta(days=1)
        df['value']= df['value'].astype(float)
        df['quantity'] = df['quantity'].astype(int)

        resultDataFrame = df.groupby(pd.Grouper(key="date", freq=self.convertTypeDate()+"-MON")).sum().reset_index()
        print(resultDataFrame.to_json())
        return resultDataFrame.to_json(date_format='iso', orient='records')
    
    
class HistoryManagement():
    def __init__(self, data,productToUpdate:Product):
        self.data = data
        self.productToUpdate = productToUpdate
        self.history = {}
    def createProduct(self):
        self.history = {
            'typeHistory': 'create',
            'valueHistory': self.data['price'] * self.data['quantity'],
            'quantityHistory': self.data['quantity'],
            'addDate': datetime.datetime.now(),
            'product': self.productToUpdate.pk
        }
        historySerializer = HistorySerializer(data=self.history)
        try:
            historySerializer.is_valid(raise_exception=True)
            historySerializer.save()
            return JsonResponse(historySerializer.data, status=201)
        except:
            return JsonResponse(historySerializer.errors, status=400)       
            
    def addProduct(self):
        self.history ={
            'typeHistory': 'buy',
            'valueHistory': self.data['price'] * self.data['quantity'],
            'quantityHistory': self.data['quantity'],
            'addDate': datetime.datetime.now(),
            'product': self.productToUpdate.pk
        }
        historySerializer = HistorySerializer(data=self.history)
        self.data['quantity'] = self.productToUpdate.quantity + self.data.get('quantity')
        productSerializer = ProductSerializer(self.productToUpdate, data=self.data, partial=True)
        try:
            productSerializer.is_valid(raise_exception=True)
            productSerializer.save()
        except:
            return JsonResponse(productSerializer.errors, status=400)
        return self.addHistory(historySerializer)
        
    def sellProduct(self):
        if self.productToUpdate is None:
            return JsonResponse({'error':'Product does not exist'}, status=400)
        if(self.data.get('price') == 0 ):
            self.history ={
                'typeHistory': 'unsold',
                'valueHistory': 0,
                'quantityHistory': self.data['quantity'],
                'addDate': datetime.datetime.now(),
                'product': self.productToUpdate.pk,
            }
            historySerialier = HistorySerializer(data=self.history)
            self.data['quantity'] = self.productToUpdate.quantity - self.data.get('quantity')
            productSerializer = ProductSerializer(self.productToUpdate, data=self.data, partial=True)
            try: 
                productSerializer.is_valid(raise_exception=True)
                productSerializer.save()
            except:
                return JsonResponse(productSerializer.errors, status=400)
            return self.addHistory(historySerialier)
        else:
            self.history ={
                'typeHistory': 'sell',
                'valueHistory': self.data['price'] * self.data['quantity'],
                'quantityHistory': self.data['quantity'],
                'addDate': datetime.datetime.now(),
                'product': self.productToUpdate.pk,
            }
            historySerializer = HistorySerializer(data=self.history)
            self.data['quantity'] = self.productToUpdate.quantity - self.data.get('quantity')
            self.data['sellArticle'] = self.productToUpdate.sellArticle + self.data.get('quantity')
            productSerializer = ProductSerializer(self.productToUpdate, data=self.data, partial=True)
            try: 
                productSerializer.is_valid(raise_exception=True)
                productSerializer.save()
            except:
                return JsonResponse(productSerializer.errors, status=400)
            return self.addHistory(historySerializer)
        
    def addHistory(self, historySerializer:HistorySerializer):
        try:
            historySerializer.is_valid(raise_exception=True)
            historySerializer.save()
            
            return JsonResponse(historySerializer.data, status=201)
        except:
            print(historySerializer.errors)
            return JsonResponse(historySerializer.errors, status=400)
    pass