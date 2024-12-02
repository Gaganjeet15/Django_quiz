# quiz/urls.py
from django.urls import path
from . import views
from .views import dashboard

urlpatterns = [
    path('', views.login_view, name='login'),  # Default route to login
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('quiz/', views.quiz, name='quiz'),
    path('reset-progress/', views.reset_progress, name='reset_progress'),
]
