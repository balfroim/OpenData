# Generated by Django 3.2 on 2021-04-17 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_registered',
            field=models.BooleanField(default=False),
        ),
    ]