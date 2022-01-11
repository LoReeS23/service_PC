from django.urls import path
from shop.views import *

urlpatterns = [
    path('', ShopView.as_view()),
    path('motherboard_buy/<int:id_num>', ShopMotherboardBuyView.as_view()),
    path('processor_buy/<int:id_num>', ShopProcessorBuyView.as_view()),
    path('graphic_buy/<int:id_num>', ShopGraphicBuyView.as_view()),
    path('disc_buy/<int:id_num>', ShopDiscBuyView.as_view()),
    path('memory_buy/<int:id_num>', ShopMemoryBuyView.as_view()),
    path('power_buy/<int:id_num>', ShopPowerSupplyBuyView.as_view()),
    path('case_buy/<int:id_num>', ShopCaseBuyView.as_view()),
    path('motherboards', MotherBoardList.as_view()),
    path('processors', ProcessorsList.as_view()),
]