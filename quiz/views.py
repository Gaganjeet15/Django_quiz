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
    current_question_id = request.POST.get('current_question_id') if request.method == "POST" else None
    
    # Handle answer submission
    if request.method == "POST" and current_question_id:
        question = Question.objects.get(id=current_question_id)
        user_answer = request.POST.get(f"question_{current_question_id}")
        is_correct = user_answer == question.correct_answer
        
        # Save the user's performance
        if request.user.is_authenticated:
            UserPerformance.objects.create(
                user=request.user,
                question=question,
                answer_given=user_answer if user_answer else '',
                is_correct=is_correct
            )
        
        # Return the same question with feedback
        questions_with_options = [{
            "id": question.id,
            "question": question.question,
            "options": [
                question.option_1,
                question.option_2,
                question.option_3,
                question.option_4,
            ],
            "feedback": {
                "is_correct": is_correct,
                "correct_answer": question.correct_answer,
                "user_answer": user_answer
            }
        }]
        
        return render(request, "quiz/quiz.html", {
            "questions": questions_with_options,
            "category": category_name if category_name else "All Categories",
            "show_next_options": True  # To show "Answer More" and "End Quiz" buttons
        })
    
    # Get a new random question
    if category_name:
        try:
            category = Category.objects.get(name=category_name)
            questions = Question.objects.filter(category=category).order_by('?')[:1]
        except Category.DoesNotExist:
            questions = []
    else:
        questions = Question.objects.all().order_by('?')[:1]

    # Prepare question data without feedback
    questions_with_options = [{
        "id": question.id,
        "question": question.question,
        "options": [
            question.option_1,
            question.option_2,
            question.option_3,
            question.option_4,
        ]
    } for question in questions]

    return render(request, "quiz/quiz.html", {
        "questions": questions_with_options,
        "category": category_name if category_name else "All Categories",
        "show_next_options": False  # Hide "Answer More" and "End Quiz" buttons initially
    })




def quiz_result(request):
    user_performance = UserPerformance.objects.filter(user=request.user)

    total_questions = user_performance.count()
    correct_answers = user_performance.filter(is_correct=True).count()

    return render(request, 'quiz/result.html', {
        'score': correct_answers,
        'total_questions': total_questions
    })