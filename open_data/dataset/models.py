from django.db import models


class Theme(models.Model):
    name = models.CharField(max_length=100, default='')
    svg_file_name = models.CharField(max_length=50, default='')

class ProxyDataset(models.Model):
    pass