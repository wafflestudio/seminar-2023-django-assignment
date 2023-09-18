from django.urls import path
from . import views

#어플리케이션의 namespace 설정
app_name = "polls"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name = 'detail'),
    path("<int:pk>/results/", views.ResultsView.as_view(), name = 'results'),
    path("<int:pk>/vote/", views.vote, name = 'vote'),
]