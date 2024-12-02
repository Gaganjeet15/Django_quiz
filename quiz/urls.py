from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Changed from dashboard to dashboard_view
    path('quiz/', views.quiz, name='quiz'),
    path('reset/', views.reset_progress, name='reset_progress'),
]