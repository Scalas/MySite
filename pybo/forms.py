from django import forms
from pybo.models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']
        labels = {
                'subject': 'subject of question',
                'content': 'question specific',
                }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
                'content': 'answer specific',
                }
