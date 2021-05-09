from collections import Counter
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup
from dictor import dictor
from django.core.management.base import BaseCommand
from django.template.loader import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.dateparse import parse_datetime
from django.utils.html import strip_tags
from open_data.settings import API_URL, TIME_ZONE, DATASETS_PER_PAGE, SPECIAL_CHARS

from dataset.models import ProxyDataset, Theme, Keyword, Datasetship
from dataset.nlp import NLP


def filter_html(url):
    # https://stackoverflow.com/a/24618186
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


def preprocess(word):
    return word.lower().replace("\"", "")


def filter_nouns(text) -> list:
    nlp = NLP.instance().nlp
    nouns = list()
    for token in nlp(text):
        if (
            len(token) <= 2 or
            any(char for char in token.lemma_ if char in SPECIAL_CHARS)
        ):
            continue
        if 'covid' in token.lemma_:
            nouns.append('covid')
            continue
        # Nom commun et nom propre
        if token.pos_ in ("NOUN", "PROPN"):
            nouns.append(preprocess(token.lemma_))
            continue
    return nouns


def generate_keywords(dataset, base_keywords, keywords_datasets):
    keywords = list()
    # From base keywords
    for base_keyword in (base_keywords or set()):
        keywords.extend(filter_nouns(base_keyword))
    # From title
    for subtitle in dataset.title.split(" - "):
        keywords.extend(filter_nouns(subtitle))
    # From description
    keywords.extend(filter_nouns(strip_tags(dataset.description)))
    # From custom view
    custom_url = "https://data.namur.be/explore/dataset/covid19be_hosp/custom/" \
                 "?disjunctive.province&disjunctive.region"
    keywords.extend(filter_nouns(filter_html(custom_url)))
    # From popularized view
    try:
        rendered = render_to_string(f'popularized/{dataset.id}.html', {'dataset': dataset})

        keywords.extend(filter_nouns(strip_tags(rendered)))
    except TemplateDoesNotExist:
        pass
    for keyword, count in Counter(keywords).most_common():
        try:
            keywords_datasets[keyword].add((dataset, count))
        except KeyError:
            keywords_datasets[keyword] = {(dataset, count)}
    return keywords_datasets


class Command(BaseCommand):
    help = 'Load datasets information from the API.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
            nb_downloads = dictor(metas, 'explore.download_count')

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
                    'nb_downloads_api': nb_downloads,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(f'{dataset_id!r} proxy dataset created.')
            else:
                self.stdout.write(f'{dataset_id!r} proxy dataset updated.')

            keywords = dictor(metas, 'default.keyword')
            keywords_datasets = generate_keywords(obj, keywords, keywords_datasets)

        self.stdout.write(self.style.SUCCESS(f'Done: {total_count} datasets, {created_count} added.'))

        for i, (keyword, datasets_occurence) in enumerate(keywords_datasets.items()):
            self.stdout.write(f'Add keywords for {datasets_occurence}. [{i}/{total_count}]')
            keyword_obj, created = Keyword.objects.get_or_create(word=keyword)
            for dataset, occurence in datasets_occurence:
                dsship = Datasetship.objects.get_or_create(keyword=keyword_obj, dataset=dataset)
                dsship.occurence = occurence
                dsship.save()

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
