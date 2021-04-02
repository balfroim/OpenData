from django import forms
from django.forms.models import ModelChoiceIterator, ModelMultipleChoiceField


# # https://medium.com/@alfarhanzahedi/customizing-modelmultiplechoicefield-in-a-django-form-96e3ae7e1a07
# class QuizModelChoiceIterator(ModelChoiceIterator):
#     def choice(self, obj):
#         return (self.field.prepare_value(obj),
#                 self.field.label_from_instance(obj), obj)
#
#
# class QuizModelChoiceField(ModelMultipleChoiceField):
#     @property
#     def choices(self):
#         if hasattr(self, '_choices'):
#             return self._choices
#         # print(list(QuizModelChoiceIterator(self)))
#         return QuizModelChoiceIterator(self)
#
#
#     # def _get_choices(self):
#     #     if hasattr(self, '_choices'):
#     #         return self._choices
#     #     return QuizModelChoiceIterator(self)
#     #
#     # choices = property(_get_choices, forms.MultipleChoiceField._set_choices)


class QuizForm(forms.Form):
    def __init__(self, quiz, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        for question in quiz.questions.all():
            self.fields.update({
                f'{question.id}': ModelMultipleChoiceField(
                    queryset=question.answers,
                    label=question.prompt,
                    widget=forms.CheckboxSelectMultiple),
            })
