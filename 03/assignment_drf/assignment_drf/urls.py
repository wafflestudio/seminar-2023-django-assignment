from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("blog.urls")),
    path('admin/', admin.site.urls),
    path('account/', include("account.urls")),
    path("api-auth/", include("rest_framework.urls")),
    #path('api/rest-auth/', include("rest_auth.urls")),
]
