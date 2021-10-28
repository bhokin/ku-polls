"""Tests of Django polls application for the question model using Django pytest."""
import datetime
from django.test import TestCase
from django.utils import timezone
from ..models import Question


class QuestionModelTests(TestCase):
    """Tests of the question model."""

    def test_was_published_recently_with_future_question(self):
        """Returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """Returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Returns True for questions whose pub_date is within the last day."""
        delta_time = datetime.timedelta(hours=23, minutes=59, seconds=59)
        time = timezone.now() - delta_time
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_past_question(self):
        """Returns False for questions whose pub_date was passed."""
        time = timezone.now() - datetime.timedelta(days=2)
        past_question = Question(pub_date=time)
        self.assertIs(past_question.is_published(), True)

    def test_is_published_with_future_question(self):
        """Returns False for questions whose pub_date is not arrived."""
        time = timezone.now() + datetime.timedelta(days=2)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_can_vote_with_question_is_enable_to_vote(self):
        """Returns True for questions whose current time are after the publication date and before end date."""
        pub_date = timezone.now() - datetime.timedelta(days=1)
        end_date = timezone.now() + datetime.timedelta(days=1)
        available_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(available_question.can_vote(), True)

    def test_can_vote_with_question_before_publication_date_question(self):
        """Returns False when the current time has not arrived at the publication date."""
        pub_date = timezone.now() + datetime.timedelta(days=1)
        end_date = timezone.now() + datetime.timedelta(days=10)
        ended_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(ended_question.can_vote(), False)

    def test_can_vote_with_question_after_end_date_question(self):
        """Returns False when the current time passed the end date."""
        pub_date = timezone.now() - datetime.timedelta(days=10)
        end_date = timezone.now() - datetime.timedelta(days=1)
        ended_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(ended_question.can_vote(), False)
