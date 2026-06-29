from django.urls import path 
from . import views

app_name = 'social_auth'

urlpatterns = [
    path('google/callback/', views.google_callback, name='google_callback'),
    path('google/login/', views.google_login, name='google_login'),
]
