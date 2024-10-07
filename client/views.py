from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from .serializers import  ClientSerializer
import datetime
from . import models
import requests
import pandas as pd
import random



frm ='30001526'
usrnm = 'isatispooya'
psswrd ='5246043adeleh'

# sms for uuid
def SendSms(snd,txt):
    txt = f'به کارگزاری ایساتیس پویا خوش آمدید \n ورود:\n http://gift.isatispooya.com/{txt}/'
    resp = requests.get(url=f'http://tsms.ir/url/tsmshttp.php?from={frm}&to={snd}&username={usrnm}&password={psswrd}&message={txt}').json()
    print(txt)
    return resp

# create uuid
class ClientViewset(APIView):
    def post (self,request):
        mobile = request.data.get('mobile')
        if not mobile:
            return Response({'error':'لطفا شماره موبایل خود را وارد کنید'},status=status.HTTP_400_BAD_REQUEST)
        client = models.Client.objects.filter(mobile=mobile).first()
        if client:
            return Response({'error':'این شماره موبایل قبلا ثبت شده است'},status=status.HTTP_400_BAD_REQUEST)
        else : 
            client = models.Client.objects.create(mobile=mobile)
            serializer =ClientSerializer(client)
            SendSms(mobile,client.uuid)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



# check uuid
class CheckUuidViewset(APIView) :
    def get (self, request, uuid):
        try:
            client = models.Client.objects.filter(uuid=uuid , gift= None)
        except:
            return Response({'error':'کد گیف وارد شده معتبر نیست'},status=status.HTTP_400_BAD_REQUEST)
        if not client.exists():
            return Response({'error':'کد گیف وارد شده معتبر نیست'},status=status.HTTP_400_BAD_REQUEST)
        client.first()
        if not client:
            return Response({'error':'کد گیف وارد شده معتبر نیست'},status=status.HTTP_400_BAD_REQUEST)
        
        return Response (True, status=status.HTTP_200_OK)



# sms for gift
def SendSms2(mobile, gift):
    txt = 'بازدید کننده گرامی \n'
    txt += 'هدیه شما:\n'
    txt += f'{gift}\n'  
    txt += 'برای تخصیص حداکثر تا پایان مهرماه ثبت نام خود را در کارگزاری ایساتیس پویا تکمیل کنید\n'
    resp = requests.get(
        url=f'http://tsms.ir/url/tsmshttp.php?from={frm}&to={mobile}&username={usrnm}&password={psswrd}&message={txt}'
    ).json()
    print(txt)
    return resp




# lottery and give gift
class GiftViewset(APIView):
    def post (self, request ,uuid) :
        if not uuid :
            return Response({'error':'لطفا یک کد گیف وارد کنید'},status=status.HTTP_400_BAD_REQUEST)
        try:
            client = models.Client.objects.filter(uuid=uuid)
        except:
            return Response({'error':'کد گیف وارد شده معتبر نیست'},status=status.HTTP_400_BAD_REQUEST)
        if not client.exists() :
            return Response({'error':'کد گیف وارد شده معتبر نیست'},status=status.HTTP_400_BAD_REQUEST)
        client = client.first()
        if client.gift :
            return Response({'error':'این کاربر قبلا یک کد گیف خریداری کرده است'},status=status.HTTP_400_BAD_REQUEST) 
        answer = request.data.get('answer')
        # if answer >2 or answer <= 0 or not answer  :
        #     return Response({'error':'لطفا پاسخ را به صورت عددی وارد کنید'},status=status.HTTP_400_BAD_REQUEST)

        
        exel = [{'جواب': 0, 'ویسا': 10, 'بازرگام': 5, 'مفتول': 0, 'خاتم': 0, 'ترمه': 0, 'min': 0, 'max': 35}, {'جواب': 0, 'ویسا': 10, 'بازرگام': 5, 'مفتول': 25, 'خاتم': 0, 'ترمه': 0, 'min': 35, 'max': 42}, {'جواب': 0, 'ویسا': 10, 'بازرگام': 5, 'مفتول': 25, 'خاتم': 10, 'ترمه': 10, 'min': 42, 'max': 44}, {'جواب': 0, 'ویسا': 10, 'بازرگام': 15, 'مفتول': 25, 'خاتم': 0, 'ترمه': 0, 'min': 44, 'max': 47}, {'جواب': 0, 'ویسا': 25, 'بازرگام': 25, 'مفتول': 0, 'خاتم': 0, 'ترمه': 0, 'min': 47, 'max': 87}, {'جواب': 0, 'ویسا': 25, 'بازرگام': 25, 'مفتول': 50, 'خاتم': 0, 'ترمه': 0, 'min': 87, 'max': 95}, {'جواب': 0, 'ویسا': 25, 'بازرگام': 25, 'مفتول': 50, 'خاتم': 10, 'ترمه': 10, 'min': 95, 'max': 97}, {'جواب': 0, 'ویسا': 25, 'بازرگام': 30, 'مفتول': 50, 'خاتم': 0, 'ترمه': 0, 'min': 97, 'max': 100}, {'جواب': 1, 'ویسا': 50, 'بازرگام': 30, 'مفتول': 0, 'خاتم': 0, 'ترمه': 0, 'min': 0, 'max': 35}, {'جواب': 1, 'ویسا': 50, 'بازرگام': 30, 'مفتول': 100, 'خاتم': 0, 'ترمه': 0, 'min': 35, 'max': 42}, {'جواب': 1, 'ویسا': 50, 'بازرگام': 30, 'مفتول': 100, 'خاتم': 20, 'ترمه': 10, 'min': 42, 'max': 44}, {'جواب': 1, 'ویسا': 50, 'بازرگام': 45, 'مفتول': 100, 'خاتم': 0, 'ترمه': 0, 'min': 44, 'max': 47}, {'جواب': 1, 'ویسا': 75, 'بازرگام': 40, 'مفتول': 0, 'خاتم': 0, 'ترمه': 0, 'min': 47, 'max': 87}, {'جواب': 1, 'ویسا': 75, 'بازرگام': 40, 'مفتول': 150, 'خاتم': 0, 'ترمه': 0, 'min': 87, 'max': 95}, {'جواب': 1, 'ویسا': 75, 'بازرگام': 40, 'مفتول': 150, 'خاتم': 30, 'ترمه': 30, 'min': 95, 'max': 97}, {'جواب': 1, 'ویسا': 75, 'بازرگام': 70, 'مفتول': 150, 'خاتم': 0, 'ترمه': 0, 'min': 97, 'max': 100}, {'جواب': 2, 'ویسا': 100, 'بازرگام': 60, 'مفتول': 0, 'خاتم': 0, 'ترمه': 0, 'min': 0, 'max': 75}, {'جواب': 2, 'ویسا': 100, 'بازرگام': 60, 'مفتول': 200, 'خاتم': 0, 'ترمه': 0, 'min': 75, 'max': 90}, {'جواب': 2, 'ویسا': 100, 'بازرگام': 100, 'مفتول': 200, 'خاتم': 40, 'ترمه': 40, 'min': 90, 'max': 95}, {'جواب': 2, 'ویسا': 100, 'بازرگام': 140, 'مفتول': 200, 'خاتم': 0, 'ترمه': 0, 'min': 95, 'max': 100}]
        df = pd.DataFrame(exel)
        df = df[df['جواب']==answer]
        df['max'] = df['max'].apply(int)
        df['min'] = df['min'].apply(int)
        possibility = random.randint(0,100)
        df = df[df['min'] <= possibility]
        df = df[df['max'] > possibility]
        df = df.to_dict('records')[0]
        del df['جواب']
        del df['max']
        del df['min']
        client.gift = str(df)
        client.save()
        
        SendSms2(client.mobile,client.gift)
        return Response(df, status=status.HTTP_201_CREATED)






