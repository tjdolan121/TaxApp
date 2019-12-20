from django.urls import path
from .views import *


urlpatterns = [
    path('reset_holdings/', reset_holdings_view, name='reset_holdings'),
    path('new_holding/', create_holding_view, name="new_holding"),
    path('<str:holding>/trade_shares/', trade_shares_view, name='trade_shares'),
    path('<str:holding>/', holding_view, name='holding'),
    path('', home_view, name='home')
]
