from django.contrib import admin
from .models import Category, Question, UserPerformance

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(UserPerformance)
