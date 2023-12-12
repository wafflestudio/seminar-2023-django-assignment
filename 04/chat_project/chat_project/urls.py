from django.contrib import admin
from django.urls import path, include

from chats.views import go_to_character_info

urlpatterns = [
    path('', go_to_character_info),
    path('admin/', admin.site.urls),
    path('chat/', include("chats.urls")),
]
