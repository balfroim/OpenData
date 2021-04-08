from django import forms


class QuizForm(forms.Form):
    def __init__(self, quiz, choices=None, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.auto_id = "question_%s"
        self.infos = quiz
        if not choices:
            choices = tuple(
                tuple(
                    choice + (False, "") for choice in question.answers.values_list('id', 'text')
                ) for question in quiz.questions.all()
            )
        for i, question in enumerate(quiz.questions.all()):
            question_key = str(question.id)
            choices = choices
            self.fields.update({
                question_key: forms.MultipleChoiceField(
                    choices=choices[i],
                    label=question.prompt,
                    widget=forms.CheckboxSelectMultiple,
                    required=False)
            })
