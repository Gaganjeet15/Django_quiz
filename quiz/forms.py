from django import forms
from .models import Question

class QuizForm(forms.Form):
    answer = forms.ChoiceField(choices=[], widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)

        # Set the choices dynamically based on the current question's options
        self.fields['answer'].choices = [
            (question.option_1, question.option_1),
            (question.option_2, question.option_2),
            (question.option_3, question.option_3),
            (question.option_4, question.option_4),
        ]
