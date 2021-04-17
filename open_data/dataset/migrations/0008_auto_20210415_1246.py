# Generated by Django 3.2 on 2021-04-15 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0007_auto_20210415_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='theme',
            name='name',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='theme',
            name='slug',
            field=models.CharField(max_length=256),
        ),
    ]