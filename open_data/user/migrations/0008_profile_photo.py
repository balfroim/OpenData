# Generated by Django 3.2.1 on 2021-05-06 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_user_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='', upload_to='profile'),
        ),
    ]