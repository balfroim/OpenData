# Generated by Django 3.1.7 on 2021-04-05 09:23

import colorfield.fields
import dataset.svg
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0002_auto_20210405_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', max_length=18),
        ),
        migrations.AlterField(
            model_name='theme',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='themes/', validators=[dataset.svg.validate_svg]),
        ),
    ]