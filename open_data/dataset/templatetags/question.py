from django import template
from django.urls import reverse

register = template.Library()


@register.inclusion_tag('modals/questions.html')
def questions_modal(dataset, user):
    return {"dataset": dataset, "is_registered": user.profile.is_registered}


@register.inclusion_tag('question/question_card.html')
def question_card(question, show_context_link=False):
    # context_link = reverse("dataset", kwargs={"dataset_id": question.da})
    return {"content": question.content}#, "show_context_link": show_context_link}


@register.inclusion_tag('question/answer_card.html')
def answer_card(answer, show_context_link=False):
    return {"content": answer.content, "show_context_link": show_context_link}
