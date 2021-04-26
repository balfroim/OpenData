from django import template

register = template.Library()


@register.inclusion_tag('modals/questions.html')
def questions_modal(dataset, user):
    return {"dataset": dataset, "user": user}


@register.inclusion_tag('question/question_card.html')
def question_card(question, user, context_link=None):
    return {"question": question, "content": question.content, "user": user,
            "context_link": context_link}


@register.inclusion_tag('question/answer_card.html')
def answer_card(answer, user, context_link=None):
    return {"answer": answer, "content": answer.content, "user": user,
            "context_link": context_link}
