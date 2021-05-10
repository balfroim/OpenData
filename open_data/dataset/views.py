from itertools import chain, combinations

from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import TemplateDoesNotExist
from django.views.decorators.http import require_POST

from badge.registry import BadgeCache
from dataset.nlp import NLP
from .models import Theme, ProxyDataset, Question, Content, Answer


def theme_page(request, theme_id):
    theme = get_object_or_404(Theme, id=theme_id)
    return render(request, 'theme.html', {'theme': theme})


def dataset_page(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    most_relevant_keywords = sorted(
        [(ship.keyword, ship.relevancy) for ship in dataset.datasetships.all()],
        key=lambda value: value[1],
        reverse=True
    )
    already_matched_ids = {dataset.id}
    already_matched_ids.update((link.to_dataset.all() for link in dataset.to_links.all()))
    init_nb_linked_datasets = len(already_matched_ids)
    datasets_by_keyword = dict()
    for keyword, relevancy in most_relevant_keywords:
        datasets = [d for d in keyword.datasets.all() if d.id not in already_matched_ids]
        if len(datasets) == 0:
            continue
        datasets_by_keyword[keyword] = datasets
        already_matched_ids.update([d.id for d in datasets])
        if len(datasets_by_keyword) >= 2:
            break
    if request.GET.get('origin', '') == 'quiz':
        BadgeCache.instance().possibly_award_badge('on_linked_quiz_inspect', user=request.user)
    return render(
        request,
        'dataset.html',
        context={
            'dataset': dataset,
            'nb_other_linked_datasets': len(already_matched_ids) - init_nb_linked_datasets,
            'nb_linked_datasets': len(already_matched_ids) - 1,
            'datasets_by_keyword': datasets_by_keyword
        }
    )


def search_page(request):
    nlp = NLP.instance().nlp
    print("nlp loaded")
    if "q" not in request.GET:
        return HttpResponse()
    keywords = {nlp(token.lower())[0].lemma_ for token in request.GET["q"].split(" ")}
    datasets_by_keyword = list()
    already_matched_ids = set()
    keywords_combinations = list(
        chain.from_iterable(
            map(
                lambda k: combinations(keywords, k),
                range(len(keywords), 0, -1)
            )
        )
    )
    for combination in keywords_combinations:
        matches = ProxyDataset.objects.exclude(id__in=already_matched_ids)
        for keyword in combination:
            matches = matches.filter(keywords__word=keyword)
        matches = sorted(
            matches,
            key=lambda ds: sum(ds.datasetships.get(keyword__word=kw).relevancy for kw in combination),
            reverse=True
        )
        if matches:
            datasets_by_keyword.append((combination, matches))
        already_matched_ids.update([match.id for match in matches])
    datasets_by_keyword = sorted(
        datasets_by_keyword,
        key=lambda value: (-len(value[0]), len(value[1]))
    )
    return render(
        request, 'search.html',
        context={
            "keywords": keywords,
            "datasets_by_keyword": datasets_by_keyword,
            "nb_datasets": len(already_matched_ids)
        })


def download_dataset(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id, exports__has_key='xls')
    dataset.nb_downloads_local += 1
    dataset.save()
    BadgeCache.instance().possibly_award_badge('on_dataset_download', user=request.user)
    return redirect(dataset.exports['xls'])


def popularized_page(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    try:
        response = render(request, f'popularized/{dataset_id}.html', {'dataset': dataset})
        response.headers['X-Frame-Options'] = 'sameorigin'
        return response
    except TemplateDoesNotExist:
        return HttpResponseNotFound()


@require_POST
def toggle_subscription(request, theme_id):
    theme = get_object_or_404(Theme, id=theme_id)
    subscribed = theme not in request.user.profile.theme_subscriptions.all()
    if subscribed:
        request.user.profile.theme_subscriptions.add(theme)
    else:
        request.user.profile.theme_subscriptions.remove(theme)

    BadgeCache.instance().possibly_award_badge('on_theme_subscription', user=request.user)

    return JsonResponse({
        'subscribed': subscribed,
        'n_subscriptions': theme.subscribed_users.count(),
    })


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
        'n_likes': dataset.liking_users.count(),
    })


def questions_page(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    BadgeCache.instance().possibly_award_badge('on_comment_read', user=request.user)
    return render(
        request,
        "tags/questions_list.html",
        context={
            "questions": dataset.questions,
            "is_registered": request.user.profile.is_registered
        }
    )


@require_POST
def add_question(request):
    dataset = None
    if "dataset_id" in request.GET:
        dataset = get_object_or_404(ProxyDataset, id=request.GET["dataset_id"])
    content = Content.objects.create(author=request.user.profile, text=request.POST["content"])
    Question.objects.create(dataset=dataset, content=content)
    BadgeCache.instance().possibly_award_badge('on_question_ask', user=request.user, dataset=dataset)
    if "dataset_id" in request.GET:
        return redirect('questions', dataset_id=dataset.id)
    else:
        return render(
            request,
            "tags/questions_list.html",
            context={
                "questions": Question.objects.order_by('-content__posted_at')[:5],
                "is_registered": request.user.profile.is_registered
            }
        )


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
    content = Content.objects.create(author=request.user.profile, text=request.POST["content"])
    Answer.objects.create(question=question, content=content)
    return render(request, "question/answers.html", context={"question": question})


@require_POST
def rmv_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    answer.content.deleted = True
    answer.content.save()
    return HttpResponse(status=204)
