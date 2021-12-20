from django.urls import path
from . views import *

urlpatterns = [
    
    path('', Homepage, name='homepage'),
    path('lottos/', lottos_list,name='lottos_list'),
    path('lottos/<int:pk>/', lotto_detail, name='lottos_detail'),
    path('lottos/<int:pk>/participate/', ticket_get, name='ticket_get'),
    path('lottos/<int:pk>/winners/',lotto_winners,name='lotto_winner'),
    path('lottos/<int:pk>/verify-ticket/',ticket_verification,name='verify_ticket'),

]