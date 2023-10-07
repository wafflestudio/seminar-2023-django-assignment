from django.shortcuts import render

# Create your views here.
#
# 이곳에 각각의 뷰 함수를 정의하면 됩니다.             
# - View 함수는 request를 인자로 받고
#   render 함수를 호출해서 결과로 리턴 합니다.
# - render 함수는 첫번째 인자로 request를 받고,
#   두번째 인자로 렌더할 템플릿을 문자열로 받습니다.

def index(request):
    return render(request, 'cities/index.html')

def city_detail(request, city):
    path_templates = 'cities/'
    if city == 'seoul':
        path_templates += 'seoul.html'
    elif city == 'tokyo':
        path_templates += 'tokyo.html'
    elif city == 'paris':
        path_templates += 'paris.html'
    else :
        path_templates += 'index.html'
    return render(request, path_templates)

