from django.http import HttpResponseNotFound
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import TemplateDoesNotExist
from django.views.decorators.http import require_POST

from badge.registry import BadgeCache
from .models import Theme, ProxyDataset, Keyword, Comment


def theme_page(request, theme_id):
    theme = get_object_or_404(Theme, id=theme_id)
    return render(request, 'theme.html', {'theme': theme})


def dataset_page(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    return render(request, 'dataset.html', {'dataset': dataset})


def search_page(request):
    search_query = request.GET["q"]
    keywords = [Keyword.preprocess(token) for token in search_query.split(' ')]
    datasets = set()
    for keyword in keywords:
        keyword_objets = Keyword.objects.filter(word__contains=keyword).all()
        for keyword_obj in keyword_objets:
            keyword_datasets = keyword_obj.datasets.all()
            datasets.update(keyword_datasets)

    return render(request, 'search.html', context={"datasets": datasets})


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
