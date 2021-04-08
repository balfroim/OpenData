import itertools

from django import forms

from .models import Answer


def generate_choices(choices, questions, to_correct):
    corrected = []
    values = list(itertools.chain(*questions.values()))
    for key, value in choices:
        checked = str(key) in values
        state = ""
        if to_correct:
            is_correct = Answer.objects.get(id=key).is_correct
            if checked:
                state = "correct" if is_correct else "incorrect"
        corrected.append((key, value, checked, state))
    return corrected


class QuizForm(forms.Form):
    def __init__(self, quiz, questions=None, to_correct=False, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.auto_id = "question_%s"
        self.infos = quiz
        if not questions:
            questions = {}
        for question in quiz.questions.all():
            question_key = str(question.id)
            choices = generate_choices(question.answers.values_list('id', 'text'), questions, to_correct)
            self.fields.update({
                question_key: forms.MultipleChoiceField(
                    choices=choices,
                    label=question.prompt,
                    widget=forms.CheckboxSelectMultiple,
                    required=False)
            })
