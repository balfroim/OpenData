from dataset.svg import validate_svg, fill_color
from django.db import models
from django.utils.text import slugify
from colorfield.fields import ColorField


class Theme(models.Model):
    name = models.CharField(max_length=100, default='', unique=True)
    slug = models.CharField(max_length=100, default='')
    image = models.FileField(upload_to='themes/', validators=[validate_svg], null=True, blank=True)
    # TODO: changer automatiquement la couleur du svg
    color = ColorField(default='#FF0000')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super(Theme, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.image})"

        # class ProxyDataset(models.Model):
#     pass
#     # slug = models.CharField(max_length=100, default='')
#     # title = models.CharField(max_length=255, default='')
#     # theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, related_name='datasets', null=True)
#     json_dump = models.JSONField()
