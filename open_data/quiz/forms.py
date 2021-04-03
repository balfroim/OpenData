from django import forms


def is_in(dic, key, value):
    return key in dic and value in dic[key]


class QuizForm(forms.Form):
    def __init__(self, quiz, request, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.auto_id = "%s"
        self.infos = quiz
        for question in quiz.questions.all():
            question_key = f'question{question.id}'
            self.fields.update({
                question_key: forms.MultipleChoiceField(
                    choices=[
                        t + (is_in(request, question_key, str(t[0])),)
                        for t in
                        question.answers.values_list('id', 'text')],
                    label=question.prompt,
                    widget=forms.CheckboxSelectMultiple,
                    required=False)
            })
