from django import template
from django.urls import reverse

register = template.Library()


@register.inclusion_tag('modals/questions.html')
def questions_modal(dataset, user):
    return {"dataset": dataset, "user": user}


@register.inclusion_tag('question/question_card.html')
def question_card(question, user):
    return {"question": question, "content": question.content, "user": user}


@register.inclusion_tag('question/answer_card.html')
def answer_card(answer, user):
    return {"answer": answer, "content": answer.content, "user": user}
