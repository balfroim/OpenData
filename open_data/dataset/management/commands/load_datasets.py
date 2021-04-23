import requests
from dictor import dictor
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.utils.html import strip_tags

from open_data.settings import API_URL, TIME_ZONE
from dataset.models import ProxyDataset, Theme, Keyword

import spacy

DATASETS_PER_PAGE = 100
NLP = spacy.load("fr_core_news_sm")


def generate_keywords(dataset, base_keywords):
    keywords = set(base_keywords) or set()
    doc = NLP(strip_tags(dataset.title + " " + dataset.description))
    keywords.update((ent.text for ent in doc.ents))
    keywords = {Keyword.preprocess(keyword) for keyword in keywords}
    for keyword in keywords:
        obj, created = Keyword.objects.update_or_create(
            word=keyword
        )
        obj.datasets.add(dataset)
        obj.save()


class Command(BaseCommand):
    help = 'Load datasets information from the API.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):
        datasets = self.fetch_all_datasets()

        total_count = len(datasets)
        created_count = 0

        for dataset in datasets:
            links = map_links(dataset['links'])
            metas = dictor(dataset, 'dataset.metas')

            id = dictor(dataset, 'dataset.dataset_id')
            theme = dictor(metas, 'default.theme.0')
            title = dictor(metas, 'default.title')
            description = dictor(metas, 'default.description') or ''
            modified = parse_datetime(dictor(metas, 'default.modified'))
            features = dictor(dataset, 'dataset.features')
            exports = fetch_exports(links['exports'])
            popularity_score = dictor(metas, 'explore.popularity_score')

            obj, created = ProxyDataset.objects.update_or_create(
                id=id,
                defaults={
                    'theme': Theme.objects.get(name=theme) if theme else None,
                    'title': title,
                    'description': description,
                    'modified': modified,
                    'has_map': 'geo' in features,
                    'has_analysis': 'analyze' in features,
                    'has_calendar': 'calendar' in features,
                    'has_custom': 'custom_view' in features,
                    'exports': exports,
                    'popularity_score': popularity_score,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(f'{id!r} proxy dataset created.')
            else:
                self.stdout.write(f'{id!r} proxy dataset updated.')

            generate_keywords(obj, dictor(metas, 'default.keyword'))

        self.stdout.write(self.style.SUCCESS(f'Done: {total_count} datasets, {created_count} added.'))

    def fetch_all_datasets(self):
        datasets = []

        done = False
        i = 0
        while not done:
            loaded_datasets, done = fetch_datasets(i)
            datasets.extend(loaded_datasets)
            i += 1

        self.stdout.write(self.style.SUCCESS(f'{len(datasets)} datasets fetched.'))
        return datasets


def fetch_datasets(page_i):
    url = f'{API_URL}catalog/datasets' \
          f'?include_app_metas=true' \
          f'&timezone={TIME_ZONE}' \
          f'&offset={page_i * DATASETS_PER_PAGE}' \
          f'&limit={DATASETS_PER_PAGE}'

    data = requests.get(url).json()

    links = map_links(data['links'])
    datasets = data['datasets']

    return datasets, 'next' not in links


def fetch_exports(url):
    data = requests.get(url).json()

    exports = map_links(data['links'])
    del exports['self']

    return exports


def map_links(links):
    return {link['rel']: link['href'] for link in links}
