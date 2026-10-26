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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('', include('customer.urls')),
    path('', include('cart.urls')),
    path('',views.index,name="index"), 
    path('about',views.about,name="about"),
    path('watches',views.watches,name="watches"),
    path('gallery',views.gallery,name="gallery"),
    path('services',views.services,name="services"),
    path('contact',views.contact,name="contact"),
    path('antique-watch-history/', views.antique_watch_history, name='antique_watch_history'),  
    path('termsofservice', views.termsofservice, name='termsofservice'),  
    path('returnpolicy', views.returnpolicy, name='returnpolicy'),  
    path('shipping page',views.shipping_page,name="shipping_page"),
    path('user_login',views.login,name="user_login"),
    path('logout',views.logout,name="logout"),
    path('user_view',views.user_view,name='user_view'),
    path('userdelete/<int:id>',views.userdelete,name="userdelete"),
    path('userupdate/<int:id>',views.userupdate,name="userupdate"),
    path('userupdate/userupdates/<int:id>',views.userupdates,name="userupdates"),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('adminview_orders', views.adminview_orders, name='adminview_orders'),
    path('useraddedproducts', views.useraddedproducts,name="useraddedproducts"),
    path('track-order/', views.track_order, name='track_order'),
    path('brands/', views.brand_index, name='brand_index'),
    path('track_orders/', views.seller_order_tracking, name='seller_order_tracking'),
    

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
