from badge.registry import BadgeCache
from django.http import HttpResponseNotFound
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import TemplateDoesNotExist
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from dataset.management.commands.load_datasets import filter_nouns

from .models import Theme, ProxyDataset, Keyword, Comment

from collections import Counter
from itertools import repeat, chain

DATASETS_PER_PAGE = 100


def theme_page(request, theme_id):
    theme = get_object_or_404(Theme, id=theme_id)
    return render(request, 'theme.html', {'theme': theme})


def dataset_page(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    return render(request, 'dataset.html', {'dataset': dataset})


def search_page(request):
    query = request.GET["q"]
    keywords = set()
    for token in query.split(" "):
        # TODO: generate synonyms ??
        keywords.update(filter_nouns(token))
    datasets = list()
    for keyword in keywords:
        try:
            keyword_obj = Keyword.objects.get(word=keyword)
        except ObjectDoesNotExist:
            continue
        datasets.extend(keyword_obj.datasets.all())
    # TODO: ordonnée par pertinence des mots clés
    return render(request, 'search.html', context={"datasets": Counter(datasets).most_common()})


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

    BadgeCache.instance().possibly_award_badge('on_dataset_liked', user=request.user)

    return JsonResponse({'liked': liked, 'n_likes': dataset.liking_users.count()})


def comments_page(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    return render(request, "modals/comments.html",
                  context={"dataset": dataset, "is_registered": request.user.profile.is_registered})


@require_POST
def add_comment(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    author = request.user.profile
    content = request.POST["content"]
    comment = Comment.objects.create(dataset=dataset, author=author, content=content)
    comment.save()
    return comments_page(request, dataset_id)
