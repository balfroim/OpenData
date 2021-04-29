import itertools

from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import TemplateDoesNotExist
from django.views.decorators.http import require_POST
from open_data.settings import NLP

from badge.registry import BadgeCache
from .models import Theme, ProxyDataset, Question, Content, Answer


def theme_page(request, theme_id):
    theme = get_object_or_404(Theme, id=theme_id)
    return render(request, 'theme.html', {'theme': theme})


def dataset_page(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    linked_datasets_by_nb_common_keywords = dict()
    for other_dataset in ProxyDataset.objects.all():
        if other_dataset == dataset:
            continue
        nb_common_keywords = len(
            dataset.keywords.all().intersection(other_dataset.keywords.all()))
        if nb_common_keywords == 0:
            continue
        try:
            linked_datasets_by_nb_common_keywords[nb_common_keywords].add(
                other_dataset)
        except KeyError:
            linked_datasets_by_nb_common_keywords[nb_common_keywords] = {
                other_dataset}

    keys = sorted(linked_datasets_by_nb_common_keywords.keys(), reverse=True)
    linked_datasets_by_nb_common_keywords = {
        k: linked_datasets_by_nb_common_keywords[k]
        for k
        in keys
        if k > 5
    }

    nb_linked_datasets = len(
        list(itertools.chain(*linked_datasets_by_nb_common_keywords.values())))

    if request.GET.get('origin', '') == 'quiz':
        BadgeCache.instance().possibly_award_badge('on_linked_quiz_inspect',
                                                   user=request.user)

    return render(request,
                  'dataset.html',
                  {'dataset': dataset,
                   'nb_linked_datasets': nb_linked_datasets,
                   'linked_datasets_by_nb_common_keywords': linked_datasets_by_nb_common_keywords})


def sort_by_nb_keywords_then_nb_datasets(value: tuple[tuple, list]) -> tuple[int, int]:
    nb_keywords = len(value[0])
    nb_datasets = len(value[1])
    return -nb_keywords, nb_datasets


def search_page(request):
    keywords = {NLP(token.lower())[0].lemma_ for token in request.GET["q"].split(" ")}
    datasets_by_keyword_match = list()
    already_matched_ids = set()
    for i in range(len(keywords), 0, -1):
        for combination in itertools.combinations(keywords, i):
            matches = ProxyDataset.objects.exclude(id__in=already_matched_ids)
            for keyword in combination:
                matches = matches.filter(keywords__word=keyword)
            matches = sorted(
                matches,
                key=lambda match: sum(
                    match.datasetships.get(keyword__word=kw).relevancy for kw in
                    combination),
                reverse=True
            )
            if matches:
                datasets_by_keyword_match.append((combination, matches))
                already_matched_ids.update([match.id for match in matches])
    datasets_by_keyword_match = sorted(
        datasets_by_keyword_match,
        key=sort_by_nb_keywords_then_nb_datasets
    )
    return render(
        request, 'search.html',
        context={
            "keywords": keywords,
            "datasets_by_keyword_match": datasets_by_keyword_match,
            "nb_datasets": len(already_matched_ids)
        })


def download_dataset(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id,
                                exports__has_key='xls')
    BadgeCache.instance().possibly_award_badge('on_dataset_download',
                                               user=request.user)
    return redirect(dataset.exports['xls'])


def popularized_page(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    try:
        response = render(request, f'popularized/{dataset_id}.html',
                          {'dataset': dataset})
        response.headers['X-Frame-Options'] = 'sameorigin'
        return response
    except TemplateDoesNotExist:
        return HttpResponseNotFound()


@require_POST
def toggle_like(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    liked = dataset not in request.user.profile.liked_datasets.all()
    if liked:
        request.user.profile.liked_datasets.add(dataset)
    else:
        request.user.profile.liked_datasets.remove(dataset)

    BadgeCache.instance().possibly_award_badge('on_dataset_like', user=request.user)

    return JsonResponse({
        'liked': liked,
        'n_likes': dataset.liking_users.count()
    })


def questions_page(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    BadgeCache.instance().possibly_award_badge('on_comment_read',
                                               user=request.user)
    return render(
        request,
        "modals/questions.html",
        context={
            "dataset": dataset,
            "is_registered": request.user.profile.is_registered
        }
    )


@require_POST
def add_question(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    content = Content.objects.create(author=request.user.profile,
                                     text=request.POST["content"])
    Question.objects.create(dataset=dataset, content=content)
    BadgeCache.instance().possibly_award_badge('on_question_ask', user=request.user,
                                               dataset=dataset)
    return redirect('questions', dataset_id=dataset.id)


def question_page(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, "question_page.html", context={"question": question})


@require_POST
def rmv_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.content.deleted = True
    question.content.save()
    return HttpResponse(status=204)


@require_POST
def add_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    content = Content.objects.create(author=request.user.profile,
                                     text=request.POST["content"])
    Answer.objects.create(question=question, content=content)
    return render(request, "question/answers.html", context={"question": question})


@require_POST
def rmv_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    answer.content.deleted = True
    answer.content.save()
    return HttpResponse(status=204)
