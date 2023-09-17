'''
#from django.http import HttpResponse
#from django.template import loader
from django.shortcuts import render, get_object_or_404
#from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Choice, Question

# Create your views here.
def index(request):
    """
    # shortcut 안 쓴 버전
    # you must reconize that your ide has to encode this with utf-8 not euc-kr
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {"latest_question_list" : latest_question_list,}
    return HttpResponse(template.render(context, request))
    """
    # shortcut
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list" : latest_question_list,}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    """
    # not using shortcut
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    
    return render(request, "polls/detail.html", {"question" : question,})
    """
    question = get_object_or_404(Question, pk=question_id)

    return render(request, "polls/detail.html", {"question" : question,})
   
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question" : question,
                "error_message" : "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id, )))
 
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question" : question,})
'''
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        list = Question.objects.filter(pub_date__lte=timezone.now())
        num_list = []
        for question in list:
            if question.choice_set.count() >= 2:
                num_list.append(question.id)
        
        return Question.objects.filter(id__in=num_list).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        list =  Question.objects.filter(pub_date__lte=timezone.now())
        num_list = []

        for question in list:
            if question.choice_set.count() >= 2:
                num_list.append(question.id)
        
        return Question.objects.filter(id__in=num_list)


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_queryset(self):
        list =  Question.objects.filter(pub_date__lte=timezone.now())
        num_list = []

        for question in list:
            if question.choice_set.count() >= 2:
                num_list.append(question.id)
        
        return Question.objects.filter(id__in=num_list)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question" : question,
                "error_message" : "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id, )))
 