import requests
import spacy
from dictor import dictor
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.utils.html import strip_tags
from open_data.settings import API_URL, TIME_ZONE

from dataset.models import ProxyDataset, Theme, Keyword

DATASETS_PER_PAGE = 100

NLP = spacy.load("fr_core_news_sm")


def filter_nouns(text) -> set:
    nouns = set()
    for token in NLP(text):
        if len(token) <= 2 or '.' in token.lemma_:
            continue
        if 'covid' in token.lemma_:
            nouns.add('covid')
            continue
        if token.pos_ in ("NOUN", "PROPN"):
            nouns.add(token.lemma_.lower().replace("\"", "".replace("-", "")))
            continue
    return nouns


def generate_keywords(dataset, base_keywords, keywords_datasets):
    keywords = set()
    for base_keyword in (base_keywords or set()):
        keywords.update(filter_nouns(base_keyword))
    for subtitle in dataset.title.split(" - "):
        keywords.update(filter_nouns(subtitle))
    keywords.update(filter_nouns(strip_tags(dataset.description)))
    # TODO: custom view, popularized view and id
    # TODO: filtrer les urls, pluriels etc
    for keyword in keywords:
        try:
            keywords_datasets[keyword].add(dataset)
        except KeyError:
            keywords_datasets[keyword] = {dataset}
    return keywords_datasets


class Command(BaseCommand):
    help = 'Load datasets information from the API.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # TODO: peut être ajouter un argument no keyword ?
    def handle(self, *args, **options):
        datasets = self.fetch_all_datasets()

        total_count = len(datasets)
        created_count = 0

        # datasets = filter(lambda ds: 'covid' in dictor(ds, "dataset.dataset_id"), datasets)
        keywords_datasets = dict()
        for dataset in datasets:
            links = map_links(dataset['links'])
            metas = dictor(dataset, 'dataset.metas')

            dataset_id = dictor(dataset, 'dataset.dataset_id')
            theme = dictor(metas, 'default.theme.0')
            title = dictor(metas, 'default.title')
            description = dictor(metas, 'default.description') or ''
            modified = parse_datetime(dictor(metas, 'default.modified'))
            features = dictor(dataset, 'dataset.features')
            exports = fetch_exports(links['exports'])
            popularity_score = dictor(metas, 'explore.popularity_score')

            obj, created = ProxyDataset.objects.update_or_create(
                id=dataset_id,
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
                self.stdout.write(f'{dataset_id!r} proxy dataset created.')
            else:
                self.stdout.write(f'{dataset_id!r} proxy dataset updated.')

            keywords_datasets = generate_keywords(obj, dictor(metas, 'default.keyword'), keywords_datasets)

        self.stdout.write(self.style.SUCCESS(f'Done: {total_count} datasets, {created_count} added.'))

        for keyword, datasets in keywords_datasets.items():
            self.stdout.write(f'Add {keyword!r} keyword for {datasets}.')
            keyword_obj, created = Keyword.objects.get_or_create(word=keyword)
            for dataset in datasets:
                Keyword.datasets.through.objects.get_or_create(keyword=keyword_obj, proxydataset=dataset)

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
