# coding=utf-8
from dataset.models import ProxyDataset
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Quiz(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='quizzes_created', null=True,
                               help_text="L'auteur du quiz.")
    title = models.CharField(max_length=255, default='', help_text="Le titre du quiz.")
    dataset = models.ForeignKey(ProxyDataset, on_delete=models.CASCADE, related_name='quizzes', null=True,
                                help_text="Le dataset source.")
    created_at = models.DateTimeField(help_text="La date de création du quiz.")

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(Quiz, self).save(*args, **kwargs)

    @property
    def correct_answers_count(self):
        return sum(question.correct_answers_count for question in self.questions.all())

    @property
    def perfect_score_rate(self):
        times_taken = self.submissions.count()
        times_perfect_score = len(tuple(sub for sub in self.submissions.all() if sub.is_perfect_score))
        return (times_perfect_score / times_taken) * 100 if times_taken > 0 else 0

    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['id']

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    prompt = models.CharField(max_length=255, default='')

    @property
    def answers_count(self):
        return self.answers.count()

    @property
    def correct_answers_count(self):
        return self.answers.filter(is_correct=True).count()

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


class QuizSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes_taken",
                             help_text="L'utilisateur qui a fait la soumission.")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='submissions',
                             help_text="Le quiz en question.")
    taken_at = models.DateTimeField(help_text="La date de soumission.")
    choices = models.JSONField(default=list, help_text="Les réponses que l'utilisateur a cochées.")
    good_answers_count = models.IntegerField(default=0, help_text="Le nombre de question bien répondue.")

    def save(self, *args, **kwargs):
        if not self.id:
            self.taken_at = timezone.now()
        return super(QuizSubmission, self).save(*args, **kwargs)

    @property
    def is_perfect_score(self):
        return self.good_answers_count == self.quiz.correct_answers_count
