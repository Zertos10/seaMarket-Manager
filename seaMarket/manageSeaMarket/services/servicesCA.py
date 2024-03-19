from abc import ABC, abstractmethod
import json
from multiprocessing.managers import BaseManager
from django.http import JsonResponse
from manageSeaMarket.models import History, Product
import pandas as pd
import numpy as np
import datetime

from manageSeaMarket.serializers import HistorySerializer, ProductSerializer

class AbstractCalculation(ABC):
    @abstractmethod
    def calculate(self)->None:
        pass
class Calculation(AbstractCalculation):
    def __init__(self, typeDate:str="year",category:str="all",maxDate=None,minDate=None,typeHistory="sell"):
        self.typeDate = str(typeDate).lower().replace("'","")
        self.maxDate = maxDate
        self.minDate = minDate
        self.category = category
        self.typeHistory = typeHistory
        self.convertDate()
    def convertDate(self):
        if self.maxDate is not None:
            self.maxDate = datetime.datetime.strptime(self.maxDate, '%Y-%m-%dT%H:%M:%S.%fZ')
        if self.minDate is not None:
            self.minDate = datetime.datetime.strptime(self.minDate, '%Y-%m-%dT%H:%M:%S.%fZ')
    def convertTypeDate(self):
        
        intialDate:str = "D"
        if self.typeDate == "day":
            intialDate = "D"
        elif self.typeDate == "week":
            intialDate = "W-MON"
        elif self.typeDate == "month":
            intialDate = "MS"
        elif self.typeDate == "year":
            intialDate = "YS"
        else :
            intialDate = "YS"
        return intialDate
    def convertDataToDataFrame(self,historySerializer:HistorySerializer):
        df = pd.DataFrame({
            "date": [history['addDate'] for history in historySerializer.data],
            "value": [history['valueHistory'] for history in historySerializer.data],
            "quantity": [history['quantityHistory'] for history in historySerializer.data]
        })
        df['date'] = pd.to_datetime(df['date'])
        df['value']= df['value'].astype(float)
        df['quantity'] = df['quantity'].astype(int)
        return df
    
class RevenuesCalculation(Calculation):
    """Calcule le chiffre d'affaire d'une catégorie de produit sur une période donnée.
    """
    def __init__(self, category, typeDate:str,maxDate=None,minDate=None):
        super().__init__(typeDate,category,maxDate,minDate,typeHistory="sell")
    def calculate(self):
        if self.minDate is None:
            self.minDate = datetime.datetime.now()
            print(self.minDate)
        result = None
        if self.maxDate is None:
            result = History.objects.filter(typeHistory=self.typeHistory, product__category__nameCategory= self.category if self.category is not None else "all")
        else:
            result = History.objects.filter(addDate__range=[self.maxDate,self.minDate], typeHistory=self.typeHistory, products__category=self.category)
        historySerializer = HistorySerializer(result, many=True)
        resultDataFrame = self.convertDataToDataFrame(historySerializer=historySerializer).groupby(pd.Grouper(key="date", freq=self.convertTypeDate())).sum().reset_index()
        resultDataFrame['date'] = resultDataFrame['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        print(resultDataFrame.to_json())
        return resultDataFrame.to_json(date_format='iso', orient='records',indent=4)
    

class MarginCalculation(Calculation):
    """Calcul la marges des produits vendus.
    """
    def __init__(self, category:str, typeDate:str,maxDate=None,minDate=None):
        super().__init__(category=category,typeDate=typeDate,typeHistory="",maxDate=maxDate,minDate=minDate)
        pass
    def calculate(self):
        result = History.objects.filter(typeHistory__in=["sell","buy","create"], product__category__nameCategory=self.category)
        if result is None:
            return JsonResponse({'error':'The category does not exist'}, status=400)
        historySerializer = HistorySerializer(result, many=True)
        convert =self.convertDataToDataFrame(historySerializer=historySerializer)
        convert['type'] = [history['typeHistory'] for history in historySerializer.data]
        convert['value'] = convert.apply(lambda row: -row['value'] if row['type'] == 'buy' or row['type'] == 'create' else row['value'], axis=1)
        convert =convert.groupby(pd.Grouper(key="date", freq=self.convertTypeDate()))['value'].sum(numeric_only=True).reset_index()
        convert['date'] = convert['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        return convert.to_json(date_format='iso', orient='records',indent=4)
    pass
class AccountingResult(MarginCalculation):
    category = "all"
    typeDate = "year"
    def __init__(self,tax=0.3):
        self.tax = tax
        super().__init__(self.category, self.typeDate)
    def __call__(self):
        result = self.calculate()
        print(result)
        result = json.loads(result)
        print(len(result))
        if result[0]['value'] >0: 
            return result[0]['value'] * self.tax
        else:
            return 0            
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