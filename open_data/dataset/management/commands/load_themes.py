import requests
from dataset.models import Theme
from dictor import dictor
from django.core.management.base import BaseCommand, CommandError
from open_data.settings import API_URL, TIME_ZONE


class Command(BaseCommand):
    help = 'Load themes from the API.'

    def handle(self, *args, **options):
        url = API_URL + 'catalog/facets?facet=theme'
        data = requests.get(url).json()
        theme_names = [dictor(facet, "name") for facet in dictor(data, "facets.0.facets")]
        for theme_name in theme_names:
            # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#get-or-create
            theme_instance, created = Theme.objects.get_or_create(name=theme_name)
            if created:
                theme_instance.save()
