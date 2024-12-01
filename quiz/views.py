from django.shortcuts import render, redirect
from .models import Question, UserPerformance
from .forms import QuizForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist

def dashboard(request):
    return render(request, 'quiz/dashboard.html')



@csrf_protect
def quiz(request):
    try:
        # Fetch all questions
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

        if request.method == 'POST':
            responses = {}
            for question_id, selected_option in request.POST.items():
                if question_id.startswith('question_'):
                    question_id = question_id.split('_')[1]  # Extract question ID
                    try:
                        question = Question.objects.get(id=question_id)
                        responses[question.id] = {
                            'selected_option': selected_option,
                            'correct_answer': question.correct_answer,
                            'is_correct': selected_option == question.correct_answer
                        }
                    except ObjectDoesNotExist:
                        return JsonResponse({'error': f"Question with ID {question_id} not found"}, status=400)

            return JsonResponse(responses, safe=False)

        # Pass all questions and options to the template
        return render(request, 'quiz/quiz.html', {'questions': questions_with_options})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def quiz_result(request):
    user_performance = UserPerformance.objects.filter(user=request.user)

    total_questions = user_performance.count()
    correct_answers = user_performance.filter(is_correct=True).count()

    return render(request, 'quiz/result.html', {
        'score': correct_answers,
        'total_questions': total_questions
    })
