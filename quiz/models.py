from django.db import models
from django.contrib.auth.models import User

# Model to represent question categories (e.g., Programming, Math)
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

# Model to represent quiz questions
class Question(models.Model):
    CATEGORY_CHOICES = [
        ('Python', 'Python'),
        ('Java', 'Java'),
        ('C', 'C'),
        ('Math', 'Math'),
        # Add more categories as needed
    ]
    
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    
    question_text = models.TextField()
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES)
    
    def __str__(self):
        return self.question_text

# Model to track user's performance in quizzes
class UserPerformance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_given = models.CharField(max_length=255)
    is_correct = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"User: {self.user.username}, Question: {self.question.id}, Correct: {self.is_correct}"
