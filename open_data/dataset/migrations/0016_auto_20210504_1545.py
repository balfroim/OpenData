# Generated by Django 3.2 on 2021-05-04 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0015_datasetlink_newsarticle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datasetlink',
            name='to_dataset',
        ),
        migrations.AddField(
            model_name='datasetlink',
            name='to_dataset',
            field=models.ManyToManyField(blank=True, related_name='from_links', to='dataset.ProxyDataset'),
        ),
    ]
