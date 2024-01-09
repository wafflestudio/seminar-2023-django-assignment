import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text,days):
    time = timezone.now()+datetime.timedelta(days=days)
    return Question.objects.create(question_text = question_text,pub_date = time)

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        #was_published_recently()가 미래 시점 Question에 대해 False 리턴하게
        time = timezone.now()+datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(),False)

    def test_was_published_recently_with_old_question(self):
        # pub_date이 하루 이상 전이면 False 리턴
        time = timezone.now()-datetime.timedelta(days=1,seconds=1)
        old_question = Question (pub_date = time)
        self.assertIs(old_question.was_published_recently(),False)

    def test_was_published_recently_with_recent_question(self):
        #pub_date이 하루 이내면 True 리턴
        time = timezone.now() - datetime.timedelta(hours = 23, minutes = 59, seconds = 59)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(),True)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        #when there are no questions
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')

        self.assertQuerySetEqual(response.context['latest_question_list'],[])

    def test_past_question(self):
        #pub_date이 과거인 애들만 display
        question = create_question(question_text = 'Past Question', days = -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        #pub_date이 미래이면 index에 display x
        create_question(question_text = 'Future Question', days = 30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerySetEqual(response.context['latest_question_list'],[])

    def test_future_question_and_past_question(self):
        #과거 질문이랑 미래 질문 둘 다 있을 때 과거 질문만 display
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        #과거 질문이 두개일때 둘 다 display 하는지 check
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )