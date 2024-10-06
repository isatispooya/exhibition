from django.urls import path
from .views import ClientViewset ,GiftViewset
urlpatterns = [

    path('get/mobile/', ClientViewset.as_view(), name='get-mobile'),
    path('gift/<str:uuid>/', GiftViewset.as_view(), name='gift'),

]