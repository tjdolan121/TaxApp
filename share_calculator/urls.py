from django.urls import path
from .views import *


urlpatterns = [
    path('account_setup/', account_setup_view, name='account_setup'),
    path('reset_holdings/', reset_holdings_view, name='reset_holdings'),
    path('new_holding/', create_holding_view, name="new_holding"),
    path('<str:holding>/trade_shares/', trade_shares_view, name='trade_shares'),
    path('<str:holding>/', holding_view, name='holding'),
    path('', home_view, name='home')
]
