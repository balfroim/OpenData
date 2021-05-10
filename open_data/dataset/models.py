import math

from colorfield.fields import ColorField
from django.db import models
from django.template.loader import TemplateDoesNotExist, get_template
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from open_data.settings import IFRAME_URL

from user.models import Profile
from .svg import validate_svg


class Theme(models.Model):
    name = models.CharField(max_length=256, unique=True)
    hidden = models.BooleanField(default=False)

    icon = models.CharField(max_length=4, default='', blank=True)
    image = models.FileField(upload_to='themes/', validators=[validate_svg], null=True, blank=True)
    color = ColorField(default='#ff0000')

    subscribed_users = models.ManyToManyField(Profile, related_name='theme_subscriptions',
                                              blank=True)

    @classmethod
    def get_displayed(cls):
        return cls.objects.filter(hidden=False)

    def popular_datasets(self):
        return self.datasets.order_by('-popularity_score')[:7]

    def __str__(self):
        return f'{self.icon} {self.name}{" (hidden)" if self.hidden else ""}'


class ProxyDataset(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    theme = models.ForeignKey(Theme, null=True, on_delete=models.SET_NULL, related_name='datasets')

    title = models.CharField(max_length=256)
    description = models.CharField(max_length=2048, default='')
    modified = models.DateTimeField(auto_now_add=True)
    exports = models.JSONField()

    has_map = models.BooleanField(default=False)
    has_analysis = models.BooleanField(default=False)
    has_calendar = models.BooleanField(default=False)
    has_custom = models.BooleanField(default=False)

    liking_users = models.ManyToManyField(Profile, related_name='liked_datasets', blank=True)
    popularity_score = models.IntegerField(default=0, editable=False)
    nb_downloads_api = models.IntegerField(default=0, editable=False)
    nb_downloads_local = models.IntegerField(default=0, editable=False)

    @property
    def nb_downloads_total(self):
        return self.nb_downloads_local + self.nb_downloads_api

    def __str__(self):
        return self.title if self.title else self.id

    @property
    def multiline_title(self):
        return mark_safe(self.title.replace(' - ', '<br>'))

    @property
    def has_table(self):
        return not (self.has_map or self.has_calendar or self.has_custom)

    @property
    def has_popularized(self):
        try:
            get_template(f'popularized/{self.id}.html')
            return True
        except TemplateDoesNotExist:
            return False

    @property
    def iframes(self):
        if self.has_popularized:
            yield 'popularized', 'fas fa-chalkboard-teacher', self.popularized_url
        if self.has_custom:
            yield 'custom', 'fas fa-info-circle', self.custom_url
        if self.has_calendar:
            yield 'calendar', 'fas fa-calendar-alt', self.calendar_url
        if self.has_map:
            yield 'map', 'fas fa-map', self.map_url
        if self.has_table:
            yield 'table', 'fas fa-table', self.table_url
        if self.has_analysis:
            yield 'analysis', 'fas fa-chart-pie', self.analysis_url

    @property
    def table_url(self):
        return f'{self.iframe_url}table'

    @property
    def map_url(self):
        return f'{self.iframe_url}map/?location=12,50.45495,4.88194'

    @property
    def analysis_url(self):
        return f'{self.iframe_url}analyze/?'

    @property
    def calendar_url(self):
        return f'{self.iframe_url}calendar/?calendarview=month&static=false'

    @property
    def custom_url(self):
        return f'{self.iframe_url}custom/'

    @property
    def popularized_url(self):
        return reverse('popularized', kwargs={"dataset_id": self.id})

    @property
    def iframe_url(self):
        return f'{IFRAME_URL}{self.id}/'


class Keyword(models.Model):
    datasets = models.ManyToManyField(
        ProxyDataset,
        related_name='keywords',
        blank=True,
        through='Datasetship'
    )
    word = models.CharField(max_length=64, primary_key=True)

    @property
    def inverse_document_frequency(self):
        # https://en.wikipedia.org/wiki/Tf–idf#Inverse_document_frequency_2
        nb_datasets = ProxyDataset.objects.count()
        occurence_in_corpus = self.datasets.count()
        return math.log(nb_datasets / occurence_in_corpus)

    def __str__(self):
        return self.word


# The relationship between a keyword and a dataset
class Datasetship(models.Model):
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name="datasetships")
    dataset = models.ForeignKey(ProxyDataset, on_delete=models.CASCADE, related_name="datasetships")
    occurence = models.IntegerField(default=0.0)

    @property
    def term_frequency(self):
        # Log normalization (https://en.wikipedia.org/wiki/Tf–idf#Term_frequency_2)
        return math.log(1 + self.occurence)

    @property
    def relevancy(self):
        """Relevance of this keyword for this dataset (tf-idf)"""
        # https://en.wikipedia.org/wiki/Tf–idf
        return self.term_frequency * self.keyword.inverse_document_frequency

    def __repr__(self):
        return f'{self.dataset!r} -(*{self.occurence})- {self.keyword!r}'

    class Meta:
        unique_together = (('keyword', 'dataset'),)


class Content(models.Model):
    author = models.ForeignKey(Profile, related_name="contents", on_delete=models.SET_NULL,
                               null=True, blank=True)
    deleted = models.BooleanField(default=False)
    text = models.TextField(max_length=512)
    posted_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.posted_at = timezone.now()
        return super(Content, self).save(*args, **kwargs)

    def display_text(self):
        return self.text if not self.deleted else mark_safe("<i>Cette question a été supprimée</i>")

    def display_author(self):
        if self.author and self.author.user.is_active:
            return self.author.name
        return mark_safe("<i>Cet utilisateur a été supprimé</i>")

    def __str__(self):
        return f"[{self.posted_at}] {self.display_author()} : {self.display_text()}"


class Question(models.Model):
    dataset = models.ForeignKey(ProxyDataset, related_name="questions", on_delete=models.CASCADE,
                                null=True, blank=True)
    content = models.OneToOneField(Content, related_name="question", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.content)


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    content = models.OneToOneField(Content, related_name="answer", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.content)


class NewsArticle(models.Model):
    dataset = models.ForeignKey(ProxyDataset, on_delete=models.CASCADE, related_name="articles")
    titre = models.TextField(max_length=512)
    link = models.URLField()
    date = models.DateTimeField()

    def __str__(self):
        return f'[{self.date}] {self.titre}'


class DatasetLink(models.Model):
    from_dataset = models.ForeignKey(ProxyDataset, on_delete=models.CASCADE, related_name="to_links")
    to_dataset = models.ManyToManyField(ProxyDataset, related_name="from_links", blank=True)
    text = models.CharField(max_length=512, default="")
