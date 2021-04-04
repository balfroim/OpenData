from django.db import models


class Theme(models.Model):
    name = models.CharField(max_length=100, default='')
    svg_file_name = models.CharField(max_length=50, default='', null=True)


# class ProxyDataset(models.Model):
#     # slug = models.CharField(max_length=100, default='')
#     # title = models.CharField(max_length=255, default='')
#     # theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, related_name='datasets', null=True)
#     json_dump = models.JSONField()
