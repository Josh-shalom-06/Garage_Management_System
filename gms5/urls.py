"""
URL configuration for gms3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from garage import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customer/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('customer/create/', views.customer_create, name='customer_create'),
    path('customer/edit/<int:customer_id>/', views.customer_edit, name='customer_edit'),
    path('customer/delete/<int:customer_id>/', views.customer_delete, name='customer_delete'),

    path('mechanics/', views.mech_list, name='mech_list'),
    path('mechanic/<int:pk>/', views.mech_detail, name='mech_detail'),
    path('mechanic/create/', views.mech_create, name='mech_create'),
    path('mechanic/edit/<int:mech_id>/', views.mech_edit, name='mech_edit'),
    path('mechanic/delete/<int:mech_id>/', views.mech_delete, name='mech_delete'),
    
    path('cars/', views.car_list, name='car_list'),
    path('car/create/', views.car_create, name='car_create'),
    path('car/edit/<int:car_id>/',views.car_edit,name='car_edit'),
    path('car/<int:pk>/', views.car_detail, name='car_details'), 
    
    path('service_records/', views.service_record_list, name='service_record_list'),
    path('service_record/create/', views.service_record_create, name='service_record_create'),
    path('service_record/checkout/<int:service_record_id>/', views.generate_invoice, name='generate_invoice'),

    path('mygarage/',views.mygarage,name='mygarage'),
    path('mygarage/stocks/',views.spareslist,name='stock_list'),
    path('mygarage/stocks/create/',views.stock_create,name='stock_create'),
    path('mygarage/stocks/update/<int:pk>/',views.stock_edit,name='stock_update'),
    path('update_stock_quantity/', views.update_stock_quantity, name='update_stock_quantity'),
    path('update-stock/', views.update_stock_quantity, name='update_stock_quantity'),
    path('service_record/complete/<int:service_record_id>/', views.complete_service, name='complete_service'),

]
