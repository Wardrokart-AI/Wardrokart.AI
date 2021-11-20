from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_customer, name='login'),
    path('register/', views.register_customer, name='register'),
    path('logout/', views.logout_customer , name='logout'),


]
