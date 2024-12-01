# quiz/urls.py
from django.urls import path
from . import views
from .views import dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('quiz/', views.quiz, name='quiz'),
    path('result/', views.quiz_result, name='quiz_result'),  # Result page
]
