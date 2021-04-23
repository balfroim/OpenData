import requests
from dictor import dictor
from django.core.management.base import BaseCommand, CommandError

from open_data.settings import API_URL, TIME_ZONE
from dataset.models import Theme


class Command(BaseCommand):
    help = 'Load themes from the API.'

    def handle(self, *args, **options):
        url = f'{API_URL}catalog/facets?facet=theme'
        data = requests.get(url).json()

        themes = [dictor(facet, 'name') for facet in dictor(data, 'facets.0.facets')]

        total_count = len(themes)
        created_count = 0

        for theme in themes:
            obj, created = Theme.objects.get_or_create(name=theme)
            if created:
                created_count += 1
                self.stdout.write(f'{obj.slug} theme created.')

        self.stdout.write(self.style.SUCCESS(f'Done: {total_count} themes, {created_count} added.'))
