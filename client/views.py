from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from . import serializers
import datetime
from . import models
import requests



frm ='30001526'
usrnm = 'isatispooya'
psswrd ='5246043adeleh'


def SendSms(snd,txt):
    txt = f'به کارگزاری ایساتیس پویا خوش آمدید \n لینک سوالات: {txt}'
    resp = requests.get(url=f'http://tsms.ir/url/tsmshttp.php?from={frm}&to={snd}&username={usrnm}&password={psswrd}&message={txt}').json()
    print(txt)
    return resp


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







