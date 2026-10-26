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
    path('product_register',views.product_register,name="product_register"),
    path('product_view/',views.product_view,name="product_view"),
    path('productdelete/<int:id>',views.productdelete,name="productdelete"),
    path('productupdate/<int:id>',views.productupdate,name="productupdate"),
    path('productupdate/productupdates/<int:id>',views.productupdates,name="productupdates"),
    path('productupdate/productupdates/<int:id>/delete_image/<int:image_id>/', views.delete_additional_image, name='delete_additional_image'),
    path('user_products', views.user_products,name="user_products"),
    path('productdeleteu/<int:id>',views.productdeleteu,name="productdeleteu"),
    path('productupdateu/<int:id>',views.productupdateu,name="productupdateu"),
    path('productupdateu/productupdate_user/<int:id>',views.productupdate_user,name="productupdate_user"),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
   
]
 

