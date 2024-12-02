from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import UserPerformance, Category, Question

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard
    return render(request, 'quiz/login.html')

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('admin:login')
        
    user_performances = UserPerformance.objects.filter(user=request.user)
    total_questions = user_performances.count()
    correct_answers = user_performances.filter(is_correct=True).count()
    accuracy = round((correct_answers / total_questions * 100) if total_questions > 0 else 0)
    
    return render(request, "quiz/dashboard.html", {
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "accuracy": accuracy,
        "categories": Category.objects.all(),
    })

def reset_progress(request):
    if request.user.is_authenticated and request.method == "POST":
        UserPerformance.objects.filter(user=request.user).delete()
        return redirect('dashboard')
    return redirect('admin:login')

@csrf_protect
def quiz(request):
    category_name = request.GET.get('category', None)
    new_quiz = request.GET.get('new_quiz', False)
    
    if request.method == "GET":
        if new_quiz or 'quiz_questions' not in request.session:
            if category_name and category_name != 'All Categories':
                try:
                    category = Category.objects.get(name=category_name)
                    db_questions = list(Question.objects.filter(
                        category=category
                    ).order_by('?')[:10])
                except Category.DoesNotExist:
                    db_questions = []
            else:
                db_questions = list(Question.objects.all().order_by('?')[:10])

            # Store fresh questions in session
            request.session['quiz_questions'] = [{
                'id': q.id,
                'question': q.question,
                'option_1': q.option_1,
                'option_2': q.option_2,
                'option_3': q.option_3,
                'option_4': q.option_4,
                'correct_answer': q.correct_answer,
                'options': [q.option_1, q.option_2, q.option_3, q.option_4],
                'user_answer': None,
                'is_correct': None,
                'difficulty': q.difficulty
            } for q in db_questions]
            request.session.modified = True
    
    # Get questions from session
    questions = request.session.get('quiz_questions', [])
    
    if request.method == "POST" and questions:  # Only process POST if we have questions
        for question in questions:
            user_answer = request.POST.get(f'question_{question["id"]}')
            if user_answer:
                is_correct = user_answer == question['correct_answer']
                
                if request.user.is_authenticated:
                    UserPerformance.objects.create(
                        user=request.user,
                        question=Question.objects.get(id=question['id']),
                        answer_given=user_answer,
                        is_correct=is_correct
                    )
                
                question['user_answer'] = user_answer
                question['is_correct'] = is_correct
        
        request.session['quiz_questions'] = questions
        request.session.modified = True
    
    return render(request, 'quiz/quiz.html', {
        'questions': questions,
        'category': category_name if category_name else "All Categories",
        'show_results': request.method == "POST",
        'total_questions': len(questions)
    })


