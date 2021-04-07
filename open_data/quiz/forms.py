from django import forms

from .models import Question


# def is_in(choice, request):
#     key, _ = choice
#     a = key in request and str(key) in request.getlist(key)
#     # print(key, a)
#     # print(request)
#     return choice + (a,)

# def correct():
#     correct_answers = []



class QuizForm(forms.Form):
    def __init__(self, quiz, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.auto_id = "question_%s"
        self.infos = quiz
        for question in quiz.questions.all():
            question_key = str(question.id)
            choices = [choice + (False, "") for choice in question.answers.values_list('id', 'text')]
            self.fields.update({
                question_key: forms.MultipleChoiceField(
                    choices=choices,
                    label=question.prompt,
                    widget=forms.CheckboxSelectMultiple,
                    required=False)
            })

    # def correct(self, request):
    #     self.infos.times_taken += 1
    #     success = True
    #     for key, field in self.fields.items():
    #         question = Question.objects.get(id=key)
    #         for i, answer in enumerate(question.answers.all()):
    #             success = success and field.choices[i][2] == answer.is_correct
    #     if success:
    #         self.infos.times_perfect_score += 1
    #     print(self.infos.times_taken, self.infos.times_perfect_score)
    #     self.infos.save()
    #     return success
