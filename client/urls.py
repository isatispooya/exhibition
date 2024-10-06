from django.urls import path
from .views import ClientViewset
urlpatterns = [

    path('get/mobile/', ClientViewset.as_view(), name='get-mobile'),

]