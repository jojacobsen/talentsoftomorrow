
from django import forms
from questionnaire.models import Submission, Answer, Question


class SubmissionCreateForm(forms.Form):
    date = forms.DateField(required=True)

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(SubmissionCreateForm, self).__init__(*args, **kwargs)

        for i, question in enumerate(extra):
            if question.question_type == 'comment':
                pass
            elif question.question_type == 'number':
                self.fields[question.slug] = forms.FloatField(label=question.text, required=question.required)
            elif question.question_type == 'range':
                self.fields[question.slug] = forms.IntegerField(label=question.text, required=question.required)
            else:
                self.fields[question.slug] = forms.CharField(label=question.text, required=question.required)

    def save(self, player, questionnaire):
        date = self.cleaned_data.pop('date')
        submission = Submission.objects.create(date=date, player=player, questionnaire=questionnaire)
        for key, value in self.cleaned_data.items():
            question = Question.objects.get(slug=key)
            answer = Answer.objects.create(submission=submission, date=date, question=question, answer=value)
