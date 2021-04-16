import requests
from dictor import dictor
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

from open_data.settings import API_URL, TIME_ZONE
from dataset.models import ProxyDataset, Theme

DATASETS_PER_PAGE = 100


class Command(BaseCommand):
    help = 'Load datasets information from the API.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):
        datasets = self.load_all_datasets()

        total_count = len(datasets)
        created_count = 0

        for dataset in datasets:
            metas = dictor(dataset, 'dataset.metas')
            id = dictor(dataset, 'dataset.dataset_id')
            theme = dictor(metas, 'default.theme.0')
            title = dictor(metas, 'default.title')
            description = dictor(metas, 'default.description') or ''
            modified = parse_datetime(dictor(metas, 'default.modified'))
            features = dictor(dataset, 'dataset.features')
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
                    'popularity_score': popularity_score,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(f'{id!r} proxy dataset created.')
            else:
                self.stdout.write(f'{id!r} proxy dataset updated.')

        self.stdout.write(self.style.SUCCESS(f'Done: {total_count} datasets, {created_count} added.'))

    def load_all_datasets(self):
        datasets = []

        done = False
        page = 0
        while not done:
            loaded_datasets, done = self.load_datasets(page)
            datasets.extend(loaded_datasets)
            page += 1

        self.stdout.write(self.style.SUCCESS(f'{len(datasets)} datasets fetched.'))
        return datasets

    def load_datasets(self, page):
        url = f'{API_URL}catalog/datasets' \
              f'?include_app_metas=true' \
              f'&timezone={TIME_ZONE}' \
              f'&offset={page * DATASETS_PER_PAGE}' \
              f'&limit={DATASETS_PER_PAGE}'

        data = requests.get(url).json()
        datasets = dictor(data, 'datasets')

        return datasets, len(datasets) < DATASETS_PER_PAGE
