# Generated by Django 3.2 on 2021-04-20 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default=None, max_length=254, null=True, unique=True, verbose_name='Adresse électronique'),
        ),
    ]
