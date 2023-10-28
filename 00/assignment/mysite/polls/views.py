from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic #제너릭 뷰는 좀 더 concise한 코드에 기여
from django.utils import timezone

from .models import Question, Choice



def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    #output = ", ".join([q.question_text for q in latest_question_list])
    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    #return HttpResponse(template.render(context, request))
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    #return HttpResponse("You're looking at question %s."% question_id)

    '''
    try:
        question = Question.objects.get(pk = question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {'question': question})
    '''

    question = get_object_or_404(Question, pk = question_id)
    return render(request, "polls/detail.html", {"question": question})
    #비슷한 함수 - get_list_or_404() 는 filter()를 써서 리스트가 비어있을 경우 Http404 예외

def results(request, question_id):
    #response = "You're looking at the results of question %s."
    #return HttpResponse(response %question_id)
    question = get_object_or_404(Question, pk = question_id)
    return render(request, "polls/results.html", {'question': question})


# 위는 제너릭 뷰 사용하지 않는 버전

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        #return the last five published questions
        #return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'




def vote(request, question_id):
    #return HttpResponse("You're voting on question %s." %question_id)
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results",args = (question.id,)))
