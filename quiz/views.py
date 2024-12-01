from django.shortcuts import render, redirect
from .models import Question, UserPerformance, Category
from .forms import QuizForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist

def dashboard(request):
    categories = Category.objects.all()  # Fetch all categories
    total_questions = Question.objects.count()
    correct_answers = 0  # Replace with your logic for correct answers
    accuracy = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    return render(request, 'quiz/dashboard.html', {
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'accuracy': accuracy,
        'categories': categories,  # Pass categories to the template
    })


@csrf_protect
def quiz(request):
    category_name = request.GET.get('category', None)

    # Filter questions by category name
    if category_name:
        try:
            category = Category.objects.get(name=category_name)
            questions = Question.objects.filter(category=category)
        except Category.DoesNotExist:
            questions = []
    else:
        questions = Question.objects.all()

    # Prepare questions with their options
    questions_with_options = [
        {
            'id': question.id,
            'question': question.question,
            'options': [question.option_1, question.option_2, question.option_3, question.option_4],
        }
        for question in questions
    ]

    return render(request, 'quiz/quiz.html', {
        'questions': questions_with_options,
        'category': category_name if category_name else "All Categories",
    })


def quiz_result(request):
    user_performance = UserPerformance.objects.filter(user=request.user)

    total_questions = user_performance.count()
    correct_answers = user_performance.filter(is_correct=True).count()

    return render(request, 'quiz/result.html', {
        'score': correct_answers,
        'total_questions': total_questions
    })
