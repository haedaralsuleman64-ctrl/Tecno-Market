from django.urls import path 
from . import views 

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name = 'order_list'),
    path('<int:order_id>/', views.order_detail, name = 'order_detail'),
    path('<int:order_id>/update-status/', views.order_update_status, name = 'update_status'),
    path('create/', views.order_create , name = 'order_create'),
    
]