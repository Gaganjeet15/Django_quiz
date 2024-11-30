from django.shortcuts import render
from .models import Question, UserPerformance
from django.contrib.auth.models import User

# Dashboard view (to show the landing page for the quiz)
def dashboard(request):
    return render(request, 'quiz/dashboard.html')

# Quiz view (to display the question and handle the quiz submission)
def quiz(request):
    question = Question.objects.order_by('?').first()  # Get a random question

    if request.method == 'POST':
        selected_option = request.POST.get('answer')  # Get the selected option from the form
        is_correct = selected_option == question.correct_answer  # Check if the selected answer is correct

        # Optionally, store the user's performance (if required)
        if request.user.is_authenticated:
            UserPerformance.objects.create(
                user=request.user,
                question=question,
                answer_given=selected_option,
                is_correct=is_correct
            )

        return render(request, 'quiz/quiz.html', {
            'question': question,
            'is_correct': is_correct
        })

    return render(request, 'quiz/quiz.html', {'question': question})
