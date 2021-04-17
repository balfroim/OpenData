from django.db import models
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from colorfield.fields import ColorField

from .svg import validate_svg
from open_data.settings import IFRAME_URL
from user.models import Profile


class Theme(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.CharField(max_length=256)
    hidden = models.BooleanField(default=False)

    image = models.FileField(upload_to='themes/', validators=[validate_svg], null=True, blank=True)
    color = ColorField(default='#FF0000')  # TODO: changer automatiquement la couleur du svg

    subscribed_users = models.ManyToManyField(Profile, related_name='theme_subscriptions', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Theme, self).save(*args, **kwargs)

    def popular_datasets(self):
        return self.datasets.order_by('-popularity_score')[:5]

    def __str__(self):
        return f'{self.name}{" (hidden)" if self.hidden else ""}'


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

    def __str__(self):
        return self.title if self.title else self.id

    @property
    def multiline_title(self):
        return mark_safe(self.title.replace(' - ', '<br>'))

    @property
    def has_table(self):
        return not (self.has_map or self.has_calendar or self.has_custom)

    @property
    def iframes(self):
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
        return f'{self.iframe_url}table/?datasetcard=true'

    @property
    def map_url(self):
        return f'{self.iframe_url}map/?datasetcard=true&location=12,50.45495,4.88194'

    @property
    def analysis_url(self):
        return f'{self.iframe_url}analyze/?datasetcard=true'

    @property
    def calendar_url(self):
        return f'{self.iframe_url}calendar/?datasetcard=true&calendarview=month&static=false'

    @property
    def custom_url(self):
        return f'{self.iframe_url}custom/?datasetcard=true'

    @property
    def iframe_url(self):
        return f'{IFRAME_URL}{self.id}/'
