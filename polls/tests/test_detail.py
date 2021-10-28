"""Tests of Django polls application using django pytest."""
import datetime
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from ..models import Question


def create_question(question_text, days):
    """Create a question by question_text and published date."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionDetailViewTests(TestCase):
    """Tests of the question detail view."""

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future returns a 404 not found."""
        future_question = create_question(
            question_text='Future question.',
            days=5
        )
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question's text."""
        past_question = create_question(
            question_text='Past Question.',
            days=-5
        )
        past_question.end_date = timezone.now() + datetime.timedelta(days=10)
        past_question.save()
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
