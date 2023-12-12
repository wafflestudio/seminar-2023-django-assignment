from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from chats.views import go_to_character_info

schema_view = get_schema_view(
   openapi.Info(
      title="my chatbot api",
      default_version='v1',
      description="waffle hw04",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="leekyw0323@snu.ac.kr"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('chat/', include("chats.urls")),
]
