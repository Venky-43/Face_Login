# face_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('project/', views.landing, name='landing'),
    path('verify-email/<int:user_id>/', views.verify_email, name='verify_email'),
]
