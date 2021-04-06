from django import forms
from .models import Question


def is_in(dic, key, value):
    return key in dic and value in dic.getlist(key)


class QuizForm(forms.Form):
    def __init__(self, quiz, request, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.auto_id = "%s"
        self.infos = quiz
        for question in quiz.questions.all():
            question_key = str(question.id)
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

    def correct(self):
        self.infos.times_taken += 1
        success = True
        for key, field in self.fields.items():
            question = Question.objects.get(id=key)
            for i, answer in enumerate(question.answers.all()):
                success = success and field.choices[i][2] == answer.is_correct
        if success:
            self.infos.times_perfect_score += 1
        print(self.infos.times_taken, self.infos.times_perfect_score)
        self.infos.save()
        return success
