# quiz/views.py
from django.shortcuts import render

def dashboard(request):
    return render(request, 'quiz/dashboard.html')  # Path to dashboard.html
