from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cities/', include('cities.urls')),
    path('', views.index),
    path('<str:city>/', views.city_detail),
]