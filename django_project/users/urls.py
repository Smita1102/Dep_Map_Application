from django.contrib import admin
from django.conf.urls import url, include
from users.views import profile
from django.urls import path

app_name = 'users'

urlpatterns = [
    url(r'^$', view=profile,  name='register'),
]