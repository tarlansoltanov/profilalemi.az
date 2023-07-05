from django.urls import path

from . import views

app_name = 'server.apps.storage'

urlpatterns = [
    path('create/', views.create, name='create'),
    path('', views.index, name='index'),
    path('update/<int:pk>', views.update, name='update'),
    path('delete/<int:pk>', views.delete, name='delete'),
]