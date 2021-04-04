from dataset.svg import validate_svg
from django.db import models


class Theme(models.Model):
    name = models.CharField(max_length=100, default='')
    image = models.FileField(upload_to ='uploads/themes/', validators=[validate_svg], null=True, blank=True)


# class ProxyDataset(models.Model):
#     pass
#     # slug = models.CharField(max_length=100, default='')
#     # title = models.CharField(max_length=255, default='')
#     # theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, related_name='datasets', null=True)
#     json_dump = models.JSONField()
