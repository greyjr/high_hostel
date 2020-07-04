from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('get_more_tables', get_more_tables, name='get_more_tables'),
    path('get_order_form', get_order_form, name='get_order_form'),
]
