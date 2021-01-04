from django.contrib import admin
from django.urls import path,include
from home import views
from django.conf import settings
from django.contrib.auth import views as auth_views
urlpatterns = [
   
     path('', views.home, name='home'),
     path('search/', views.search, name='search'),
     path('products/', views.productss, name='products'),
     path('cart/', views.cart, name='cart'),
     path('updatecart/', views.updatecart, name='updatecart'),
     path('tracker/', views.tracker, name='tracker'),
     path('checkout/', views.checkout, name='checkout'),
     path('processorder/', views.processorder, name='processorder'),
     path('user/', views.user, name='user'),
     path('contact', views.Contact, name='contact'),
     path('single/<str:slug>',views.singleproduct,name ='singleproduct'),
     path('provider/',views.provider,name ='provider'),
     path('check/', views.check, name='check'),


     #merchant account stuff'
     path('merchant_account/', views.merchant, name='merchant_account'),
    
]