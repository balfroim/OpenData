# Generated by Django 3.2 on 2021-04-19 13:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dataset', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizsubmission',
            name='user',
            field=models.ForeignKey(help_text="L'utilisateur qui a fait la soumission.", null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quizzes_taken', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quiz',
            name='author',
            field=models.ForeignKey(help_text="L'auteur du quiz.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quizzes_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quiz',
            name='dataset',
            field=models.ForeignKey(help_text='Le dataset source.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='dataset.proxydataset'),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.quiz'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='quiz.question'),
        ),
    ]
