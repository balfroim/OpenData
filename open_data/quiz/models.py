from dataset.models import ProxyDataset
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Quiz(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, default='')
    dataset = models.ForeignKey(ProxyDataset, on_delete=models.CASCADE, related_name='quizzes', null=True)
    created_at = models.DateTimeField(editable=False)
    times_taken = models.IntegerField(default=0, editable=False)
    # Nombre de personnes qui ont un score parfait.
    times_perfect_score = models.IntegerField(default=0, editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(Quiz, self).save(*args, **kwargs)

    @property
    def question_count(self):
        return self.questions.count()

    @property
    def perfect_score_rate(self):
        return (self.times_perfect_score / self.times_taken) * 100 if self.times_taken > 0 else 0

    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['id']

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    prompt = models.CharField(max_length=255, default='')

    @property
    def answer_count(self):
        return self.answers.count()

    class Meta:
        verbose_name_plural = "Questions"
        ordering = ['id']

    def __str__(self):
        return self.prompt


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255, default='')
    is_correct = models.BooleanField()

    def __str__(self):
        return self.text
