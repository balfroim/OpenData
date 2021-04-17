# Generated by Django 3.2 on 2021-04-15 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('quiz', '0002_auto_20210408_1516'), ('quiz', '0003_auto_20210408_1633')]

    dependencies = [
        ('dataset', '0005_auto_20210405_1826_squashed_0007_auto_20210405_1904'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='dataset_id',
        ),
        migrations.AddField(
            model_name='quiz',
            name='dataset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='dataset.proxydataset'),
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='times_perfect_score',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='times_taken',
        ),
        migrations.AlterField(
            model_name='quiz',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quizzes_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.CreateModel(
            name='QuizSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taken_at', models.DateTimeField()),
                ('good_answers_count', models.IntegerField(default=0)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='quiz.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes_taken', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
