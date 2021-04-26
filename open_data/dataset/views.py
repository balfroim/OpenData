import itertools
from collections import Counter

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import TemplateDoesNotExist
from django.views.decorators.http import require_POST

from .models import Theme, ProxyDataset, Keyword, Comment
from badge.registry import BadgeCache

DATASETS_PER_PAGE = 100


def theme_page(request, theme_id):
    theme = get_object_or_404(Theme, id=theme_id)
    return render(request, 'theme.html', {'theme': theme})


def dataset_page(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    linked_datasets_by_nb_common_keywords = dict()
    for other_dataset in ProxyDataset.objects.all():
        if other_dataset == dataset:
            continue
        nb_common_keywords = len(dataset.keywords.all().intersection(other_dataset.keywords.all()))
        if nb_common_keywords == 0:
            continue
        try:
            linked_datasets_by_nb_common_keywords[nb_common_keywords].add(other_dataset)
        except KeyError:
            linked_datasets_by_nb_common_keywords[nb_common_keywords] = {other_dataset}

    keys = sorted(linked_datasets_by_nb_common_keywords.keys(), reverse=True)
    linked_datasets_by_nb_common_keywords = {
        k: linked_datasets_by_nb_common_keywords[k]
        for k
        in keys
        if k > 5
    }

    print(linked_datasets_by_nb_common_keywords)
    nb_linked_datasets = len(list(itertools.chain(*linked_datasets_by_nb_common_keywords.values())))

    if request.GET.get('origin', '') == 'quiz':
        BadgeCache.instance().possibly_award_badge('on_linked_quiz_inspect', user=request.user)

    return render(request,
                  'dataset.html',
                  {'dataset': dataset,
                   'nb_linked_datasets': nb_linked_datasets,
                   'linked_datasets_by_nb_common_keywords': linked_datasets_by_nb_common_keywords})


def search_page(request):
    query = request.GET["q"]
    keywords = set()
    for token in query.split(" "):
        # TODO: generate synonyms ??
        keywords.add(token.lower())
    datasets = list()
    for keyword in keywords:
        try:
            keyword_obj = Keyword.objects.get(word=keyword)
        except ObjectDoesNotExist:
            continue
        datasets.extend(keyword_obj.datasets.all())
    nb_datasets = len(datasets)
    # TODO: ordonnée par pertinence des mots clés ?
    datasets_by_keyword_match = dict()
    for dataset, count in Counter(datasets).most_common():
        try:
            datasets_by_keyword_match[count].add(dataset)
        except KeyError:
            datasets_by_keyword_match[count] = {dataset}
    return render(request, 'search.html',
                  context={"datasets_by_keyword_match": datasets_by_keyword_match, "nb_datasets": nb_datasets})


def popularized_page(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    try:
        response = render(request, f'popularized/{dataset_id}.html', {'dataset': dataset})
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

    return JsonResponse({'liked': liked, 'n_likes': dataset.liking_users.count()})


def comments_page(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    BadgeCache.instance().possibly_award_badge('on_comment_read', user=request.user)
    return render(request, "modals/comments.html",
                  context={"dataset": dataset, "is_registered": request.user.profile.is_registered})


@require_POST
def add_comment(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    author = request.user.profile
    content = request.POST["content"]
    comment = Comment.objects.create(dataset=dataset, author=author, content=content)
    comment.save()
    BadgeCache.instance().possibly_award_badge('on_comment_add', user=request.user)
    return comments_page(request, dataset_id)


def download_dataset(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id, exports__has_key='xls')
    BadgeCache.instance().possibly_award_badge('on_dataset_download', user=request.user)
    return redirect(dataset.exports['xls'])
