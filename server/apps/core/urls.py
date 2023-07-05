from django.urls import path

from . import views

app_name = 'server.apps.core'

urlpatterns = [
    path('', views.home, name='home'),
]