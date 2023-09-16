from django.contrib import admin
from django.urls import path
from . import views
#.은 같은 디렉토리 의미
urlpatterns = [
    path('menu/',views.index),
    path('', views.index),
    path('menu/<int:pk>/',views.food_detail),
]
