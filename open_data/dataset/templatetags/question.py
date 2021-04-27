from django import template

register = template.Library()


@register.inclusion_tag('modals/questions.html')
def questions_modal(dataset, user):
    return {"dataset": dataset, "user": user}


@register.inclusion_tag('question/question_card.html')
def question_card(question, user, show_context_link=True):
    return {
        "content": question.content,
        "user": user,
        "show_context_link": show_context_link
    }


@register.inclusion_tag('question/answer_card.html')
def answer_card(answer, user, show_context_link=True):
    return {
        "content": answer.content,
        "user": user,
        "show_context_link": show_context_link
    }


@register.inclusion_tag('question/answers.html')
def answers_of(question):
    return {
        "question": question
    }
