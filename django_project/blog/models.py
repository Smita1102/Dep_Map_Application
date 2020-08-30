from django.db import models
from django.db.models import Count
from django.utils.timezone import now
from django.contrib.auth.models import User

from .constants import REQUIRED_CHOICES
from .managers import QuestionQuerySet



class Question(models.Model):
    question_id = models.IntegerField()
    question_text = models.CharField(max_length=100)
    question_type = models.CharField(max_length=100, default="None")
    set_id = models.IntegerField()
    
    objects = QuestionQuerySet.as_manager()

    def __str__(self):
        return self.question_text

    def choices_count(self):
        return self.choices.count()

    choices_count.short_description = 'Number of choices'

    def has_enough_choices(self):
        return self.choices.count() >= REQUIRED_CHOICES

    has_enough_choices.boolean = True

    def total_votes(self):
        aggregate_dict = self.choices.aggregate(total_answers=Count('answers'))
        if aggregate_dict:
            return aggregate_dict.get('total_answers', 0)
        return 0


class Choice(models.Model):

    #question= models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    question_id = models.IntegerField()
    question_type = models.CharField(max_length=5)
    choice_text= models.CharField(max_length=200)
    set_id = models.IntegerField()
    is_valid = models.CharField(max_length=1)

   
    

    def __str__(self):
        return self.choice_text

    def votes(self):
        return self.answers.count()


class Answer(models.Model):
    answer = models.ForeignKey(Choice,
                               on_delete=models.CASCADE,
                               related_name='answers')
    session_key = models.CharField(max_length=32)
    date = models.DateTimeField(default=now)

    
class SetsAttempted(models.Model):
    user_id =  models.ForeignKey(
                    User,
                    on_delete=models.CASCADE
        )
    set_id = models.IntegerField()
    question_type = models.CharField(max_length=5)
    question_id = models.IntegerField()
    Value = models.CharField(max_length=50)
    datecreated = models.DateTimeField()


class Book(models.Model):

    name = models.CharField(max_length=255)
    isbn_number = models.CharField(max_length=13)
    user_id =  models.ForeignKey(
                    User,
                    on_delete=models.CASCADE
        )
    set_id = models.IntegerField(default='0')
    question_type = models.CharField(max_length=5, default='0')
    question_id = models.IntegerField(default='0')

    class Meta:
        db_table = 'book'

    def __str__(self):
        return self.name