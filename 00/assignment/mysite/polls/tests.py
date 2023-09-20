from django.test import TestCase
import datetime

from django.utils import timezone
from .models import Question, Choice
from django.urls import reverse
# Create your tests here.

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_futre_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)

        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recentn_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)

        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days, choice = 2):
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text=question_text, pub_date=time)
    for i in range(choice):
        Choice.objects.create(question=question, choice_text=str(i))
    return question



class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_path_question(self):
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual( response.context["latest_question_list"], [question], )

    def test_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")

        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )
    

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
    
    def no_choice_question(self):
        no_choice_question = create_question(question_text="no choice Question", days=0, choice=0)
        url = reverse("polls:detail", args=(no_choice_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def one_choice_question(self):
        one_choice_question = create_question(question_text="one choice Question", days=0, choice=1)
        url = reverse("polls:detail", args=(one_choice_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def two_choice_question(self):
        two_choice_question = create_question(question_text="two choice Question", days=0, choice=2)
        url = reverse("polls:detail", args=(two_choice_question.id,))
        response = self.client.get(url)
        self.assertContains(response, two_choice_question.question_text)


class QuestionResultsViews(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
    
    def no_choice_question(self):
        no_choice_question = create_question(question_text="no choice Question", days=0, choice=0)
        url = reverse("polls:results", args=(no_choice_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def one_choice_question(self):
        one_choice_question = create_question(question_text="one choice Question", days=0, choice=1)
        url = reverse("polls:results", args=(one_choice_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def two_choice_question(self):
        two_choice_question = create_question(question_text="two choice Question", days=0, choice=2)
        url = reverse("polls:results", args=(two_choice_question.id,))
        response = self.client.get(url)
        self.assertContains(response, two_choice_question.question_text)
