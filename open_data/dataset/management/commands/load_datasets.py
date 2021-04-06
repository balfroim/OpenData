import requests
from dictor import dictor
from django.core.management.base import BaseCommand
from open_data.settings import API_URL, TIME_ZONE
from dataset.models import ProxyDataset, Theme, ProxyDatasetStat
from django.utils.dateparse import parse_datetime
import pytz

def print_carriage(message):
    print("\r" + " " * 100, end="")
    print("\r" + message, end="")

def load_datasets(to_load_count=100, loaded_count=0):
    url = f"{API_URL}catalog/datasets?timezone={TIME_ZONE}&include_app_metas=true" \
        f"&limit={max(100, to_load_count)}&offset={loaded_count}"
    data = requests.get(url).json()
    datasets = dictor(data, "datasets")
    total_count = dictor(data, "total_count")
    loaded_count += to_load_count
    to_load_count = total_count - loaded_count
    print_carriage(f"Fetch datasets from the API [{loaded_count}/{total_count}].")
    return datasets, to_load_count, loaded_count




class Command(BaseCommand):
    help = 'Load datasets informations from the API.'

    def handle(self, *args, **options):
        datasets, to_load_count, loaded_count = load_datasets()
        while to_load_count > 0:
            _datasets, to_load_count, loaded_count = load_datasets(to_load_count, loaded_count)
            datasets += _datasets
        print_carriage("All datasets were fetched from the API.")
        total_count = len(datasets)
        for i, dataset in enumerate(datasets):
            id = dictor(dataset, "dataset.dataset_id")
            proxy_dataset, created = ProxyDataset.objects.get_or_create(id=id)
            metas = dictor(dataset, "dataset.metas")
            modified = parse_datetime(dictor(metas, "default.modified"))
            # If the dataset is created or not up to data
            if created or proxy_dataset.modified is None or modified > proxy_dataset.modified:
                proxy_dataset.modified = modified
                proxy_dataset.title = dictor(metas, "default.title")
                theme = dictor(metas, "default.theme.0")
                proxy_dataset.theme = Theme.objects.get(name=theme) if theme else None
                proxy_dataset.description = dictor(metas, "default.description")
                proxy_dataset.save()
                stat = ProxyDatasetStat.objects.create(
                    dataset = proxy_dataset,
                    popularity_score = dictor(metas, "explore.popularity_score")
                )
                stat.save()

            print_carriage(f"Load dataset {id} in the database [{i}/{total_count}].")
        print_carriage(f"All datasets are loaded in the database.")

