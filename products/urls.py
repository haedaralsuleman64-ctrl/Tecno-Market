from django.urls import path 
from . import views 
from .views import ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = 'products'

urlpatterns = [
    path('' , views.product_list , name = 'product_list'),
    path('categories/', views.category_list , name = 'category_list'),
    path('categories/<slug:category_slug>/' , views.product_list , name = 'product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail , name = 'product_detail'),
    path('my-products/', views.my_products, name='my_products'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('special_products/' , views.special_products , name = 'special_products'),
    path('help_page/' , views.help_page , name = 'help_page'),
]