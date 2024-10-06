from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from . import serializers
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
    txt = f'به کارگزاری ایساتیس پویا خوش آمدید \n لینک سوالات:\n www.isatispooya.com/{txt}/'
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
            serializer = serializers.ClientSerializer(client)
            SendSms(mobile,client.uuid)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



# check uuid
class CheckUuidViewset(APIView) :
    def get (self, request, uuid):
        client = models.Client.objects.filter(uuid=uuid , gift= None).first()
        if not client:
            return Response({'error':'کد گیف وارد شده معتبر نیست'},status=status.HTTP_400_BAD_REQUEST)
        
        return Response (True, status=status.HTTP_200_OK)



# sms for gift
def SendSms2(mobile, gift):
    txt = 'به کارگزاری ایساتیس پویا خوش آمدید \n'
    txt += 'ادرس سایت:\n www.isatispooya.com/ \n'
    txt += 'هدیه شما:\n'
    txt += f'{gift}\n'  
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
        client = models.Client.objects.filter(uuid=uuid).first()
        if not client :
            return Response({'error':'کد گیف وارد شده معتبر نیست'},status=status.HTTP_400_BAD_REQUEST)
        if client.gift :
            return Response({'error':'این کاربر قبلا یک کد گیف خریداری کرده است'},status=status.HTTP_400_BAD_REQUEST) 
        answer = request.data.get('answer')
        if answer >2 or answer < 0 or not answer  :
            return Response({'error':'لطفا پاسخ را به صورت عددی وارد کنید'},status=status.HTTP_400_BAD_REQUEST)
        
        df = pd.read_excel('book1.xlsx')
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






