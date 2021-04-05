# Generated by Django 3.1.7 on 2021-04-05 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('dataset', '0005_auto_20210405_1826'), ('dataset', '0006_auto_20210405_1838'), ('dataset', '0007_auto_20210405_1904')]

    dependencies = [
        ('dataset', '0004_proxydataset_proxydatasetstat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proxydataset',
            name='modified',
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.RemoveField(
            model_name='proxydataset',
            name='stat',
        ),
        migrations.AddField(
            model_name='proxydatasetstat',
            name='dataset',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stat', to='dataset.proxydataset'),
        ),
        migrations.AlterField(
            model_name='proxydataset',
            name='description',
            field=models.CharField(default='', max_length=255, null=True),
        ),
    ]
