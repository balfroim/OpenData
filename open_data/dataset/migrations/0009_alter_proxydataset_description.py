# Generated by Django 3.2 on 2021-04-15 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0008_auto_20210415_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proxydataset',
            name='description',
            field=models.CharField(default='', max_length=256),
        ),
    ]
