from django.shortcuts import render, redirect
from .models import Question, UserPerformance, Category
from .forms import QuizForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist

def dashboard(request):
    categories = Category.objects.all()  # Fetch all categories
    total_questions = Question.objects.count()
    
    # Get the user's performance data
    if request.user.is_authenticated:
        user_performance = UserPerformance.objects.filter(user=request.user)
        correct_answers = user_performance.filter(is_correct=True).count()  # Count correct answers for the user
    else:
        correct_answers = 0  # If the user is not authenticated, default to 0
    
    # Calculate accuracy (avoid division by zero)
    accuracy = round((correct_answers / total_questions) * 100, 2) if total_questions > 0 else 0
    
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
            questions = Question.objects.filter(category=category).order_by('?')[:10]
        except Category.DoesNotExist:
            questions = []
    else:
        questions = Question.objects.all().order_by('?')[:10]

    feedback = {}
    if request.method == "POST":
        for question in questions:
            user_answer = request.POST.get(f"question_{question.id}", None)
            is_correct = user_answer == question.correct_answer
            feedback[question.id] = {
                "user_answer": user_answer,
                "is_correct": is_correct,
                "correct_answer": question.correct_answer,
            }
        
        # Save the user's performance data
        if request.user.is_authenticated:
            for question_id, data in feedback.items():
                question = Question.objects.get(id=question_id)
                UserPerformance.objects.create(
                    user=request.user,
                    question=question,
                    answer_given=data['user_answer'] if data['user_answer'] else '',
                    is_correct=data['is_correct']
                )

    # Prepare questions with their options and feedback
    questions_with_options = [
        {
            "id": question.id,
            "question": question.question,
            "options": [
                question.option_1,
                question.option_2,
                question.option_3,
                question.option_4,
            ],
            "feedback": feedback.get(question.id),  # Attach feedback directly
        }
        for question in questions
    ]

    return render(request, "quiz/quiz.html", {
        "questions": questions_with_options,
        "category": category_name if category_name else "All Categories",
    })




def quiz_result(request):
    user_performance = UserPerformance.objects.filter(user=request.user)

    total_questions = user_performance.count()
    correct_answers = user_performance.filter(is_correct=True).count()

    return render(request, 'quiz/result.html', {
        'score': correct_answers,
        'total_questions': total_questions
    })
