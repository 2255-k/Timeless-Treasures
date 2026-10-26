"""
URL configuration for watch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('user_register',views.user_register,name="user_register"),
    path('user-profile/', views.user_profile, name='user_profile'), 
    path('order-summary/', views.order_summary, name='order_summary'),
    path('bankdetail',views.bankdetail,name="bankdetail"),
    path('notifications/', views.view_notifications, name='view_notifications'), 
    path('mark_notifications_read/', views.mark_notifications_read, name='mark_notifications_read'), 
    path('edit_shipping_address/', views.edit_shipping_address, name='edit_shipping_address'),
    path('checkedit_shipping_address/', views.checkedit_shipping_address, name='checkedit_shipping_address'),
    path('view_order', views.view_order, name='view_order'),
    path('products-bought-by-others/', views.products_bought_by_others, name='products_bought_by_others'), 
    path('userprofiledelete/', views.userprofiledelete, name='userprofiledelete'),
    

]