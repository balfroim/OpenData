# Generated by Django 3.2 on 2021-04-28 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0012_auto_20210428_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasetships',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datasetships', to='dataset.proxydataset'),
        ),
    ]
