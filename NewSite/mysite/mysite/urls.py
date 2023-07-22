# mysite/urls.py
from django.contrib import admin
from django.urls import include, path
from chat.views import *
urlpatterns = [
    path("chat/", include("chat.urls")),
    path("login/", Login, name="login"),
    path("admin/", admin.site.urls),
]