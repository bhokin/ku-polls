"""The models for Django polls application."""
import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Question(models.Model):
    """Question model for each poll question."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date', null=True, default=timezone.now)

    def was_published_recently(self):
        """Check that the question was published recently or not.

        Returns:
            bool: True if the question was published recently False otherwise
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def is_published(self):
        """Check that the question is published or not.

        Returns:
            bool: True if the question is published and False for otherwise
        """
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Check that the question can vote or not.

        Returns:
            bool: True if the question can vote and False for otherwise
        """
        now = timezone.now()
        return self.end_date >= now >= self.pub_date

    def __str__(self):
        """Return the question text.

        Returns:
            str: question text
        """
        return self.question_text


class Choice(models.Model):
    """Choice model for choice in each poll question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)

    @property
    def votes(self) -> int:
        """Return votes amount of that choice.

        Returns:
            int: votes amount
        """
        return Vote.objects.filter(choice=self).count()

    def __str__(self):
        """Return the choice text.

        Returns:
            str: choice text
        """
        return self.choice_text


class Vote(models.Model):
    """Vote model in each poll question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=0)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=0)

    def __str__(self):
        """Return the representation of vote.

        Returns:
            str: question text
        """
        return f"{self.question} has been voted with {self.choice}"
