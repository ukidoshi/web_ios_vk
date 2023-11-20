from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class QuestionsManager(models.Manager):
    def find_new_questions(self):
        return self.order_by("-creation_date")

    def find_hot_questions(self):
        return self.order_by("-question_likes")

    def find_with_tag(self, tag):
        return self.filter(tag__tag_word=tag)


class AnswerManager(models.Manager):

    def find_answers_to_question(self, question):
        return self.filter(to_question=question).order_by("-is_correct")


class TagManager(models.Manager):
    def get_popular_tags(self):
        return self.order_by("-id")[:8]


class Answer(models.Model):
    content = models.TextField()
    to_question = models.ForeignKey('Question', on_delete=models.PROTECT)
    author = models.ForeignKey('Profile', on_delete=models.PROTECT)
    creation_date = models.DateField(null=True, blank=True)

    ANSWERSTATUS = [
        (1, 'Correct'),
        (0, 'Incorrect')
    ]

    objects = AnswerManager()

    is_correct = models.IntegerField(choices=ANSWERSTATUS, null=True, blank=True)
    answer_likes = models.IntegerField(default=0)
    answer_dislikes = models.IntegerField(default=0)

    def __str__(self):
        try:
            return self.content[:10]
        except:
            return self.content

    def get_score(self):
        return self.answer_likes - self.answer_dislikes


class Tag(models.Model):
    tag_word = models.CharField(max_length=100)

    objects = TagManager()

    def __str__(self):
        return self.tag_word


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    creation_date = models.DateField(null=True, blank=True)
    email = models.CharField(max_length=256)
    nickname = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


class Question(models.Model):
    title = models.TextField()
    content = models.TextField()
    author = models.ForeignKey('Profile', on_delete=models.PROTECT)
    creation_date = models.DateField(null=True, blank=True)
    question_likes = models.IntegerField(default=0)
    question_dislikes = models.IntegerField(default=0)
    tag = models.ManyToManyField('Tag', related_name='questions', null=True, blank=True)
    objects = QuestionsManager()

    def count(self):
        return Answer.objects.find_answers_to_question(self)

    def get_score(self):
        return self.question_likes - self.question_dislikes

    def __str__(self):
        return self.title
