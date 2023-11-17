from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('posts/', views.posts, name="post"),
    path('lists/', views.lists, name="list"),
    path('lists/<int:pk>/', views.detail, name="detail"),
    path('edit/<int:pk>/', views.edit, name="edit"),
    path('edit_end/<int:pk>/', views.edit_end, name="edit_end"),
    path('create/', views.create, name="create"),
    path('add_comment/<int:pk>', views.add_comment, name="add_comment"),
    path('delete/<int:pk>', views.delete, name="delete"),
]