# Generated by Django 3.2 on 2021-05-04 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0014_rename_datasetships_datasetship'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.TextField(max_length=512)),
                ('link', models.URLField()),
                ('date', models.DateTimeField()),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='dataset.proxydataset')),
            ],
        ),
        migrations.CreateModel(
            name='DatasetLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='', max_length=512)),
                ('from_dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_links', to='dataset.proxydataset')),
                ('to_dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_links', to='dataset.proxydataset')),
            ],
        ),
    ]
