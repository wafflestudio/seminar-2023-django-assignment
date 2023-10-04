from django.shortcuts import render
from portfolio.models import Person

# Create your views here.
def index(request):
    me = Person.objects.get(name="이현오")
    context = {"me":me}
    return render(request, 'portfolio/index.html', context = context)