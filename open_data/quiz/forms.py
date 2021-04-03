from django import forms


class QuizForm(forms.Form):
    def __init__(self, quiz, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.auto_id = "%s"
        self.infos = quiz
        for question in quiz.questions.all():
            self.fields.update({
                f'{question.id}': forms.ModelMultipleChoiceField(
                    queryset=question.answers,
                    label=question.prompt,
                    widget=forms.CheckboxSelectMultiple),
            })
