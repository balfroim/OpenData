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
    def __init__(self, quiz, choices=None, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.auto_id = "question_%s"
        self.infos = quiz
        if not choices:
            choices = tuple(
                itertools.chain.from_iterable(
                    (
                        choice + (False, "") for choice in question.answers.values_list('id', 'text')
                    ) for question in quiz.questions.all()
                )
            )
        for question in quiz.questions.all():
            question_key = str(question.id)
            choices = choices
            self.fields.update({
                question_key: forms.MultipleChoiceField(
                    choices=choices,
                    label=question.prompt,
                    widget=forms.CheckboxSelectMultiple,
                    required=False)
            })
