from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="WaffleChat",
        default_version="1.1.1",
        description="까칠한 냥이 챗봇 API 문서",
    ),
    public=True,
)

urlpatterns = [
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('chat/', include("chat.urls")),
    path('__debug__/', include("debug_toolbar.urls")),
]
