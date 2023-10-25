"""
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader 
from django.urls import reverse

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    #template = loader.get_template("polls/index.html")

    context = {
        "latest_question_list" : latest_question_list,
    }
    #return HttpResponse(template.render(context, request))
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question" : question})


def results(request, question_id):
    question =  get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"qeustion" : question})

"""
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
from django.db.models import Count

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()) \
                                .annotate(choice_len=Count('choice')).filter(choice_len__gte=2)\
                                .order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())\
                                .annotate(choice_len=Count('choice')).filter(choice_len__gte=2)

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())\
                                .annotate(choice_len=Count('choice')).filter(choice_len__gte=2)


def vote(request, question_id):
    def get_queryset():
        return Question.objects.filter(pub_date__lte=timezone.now())\
                                .annotate(choice_len=Count('choice')).filter(choice_len__gte=2)
    
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        assert( question in get_queryset() )
    except:
        raise Http404("Don't access with weird way")

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except( KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question" : question,
                "error_message":"You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question_id, )))