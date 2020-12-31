from django.contrib import admin
from django.urls import path,include
from items import views
from django.conf import settings
from django.contrib.auth import views as auth_views
urlpatterns = [
   



     
     path('signin', views.signin, name='signin'),
     path('login', views.login, name='login'),
     path('logout', views.logouts, name='logout'),
]