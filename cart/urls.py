from django.urls import path
from . import views



app_name = 'cart'

urlpatterns = [
    path('<int:product_productid>/add/',views.cart_add , name='cart_add'),

]
