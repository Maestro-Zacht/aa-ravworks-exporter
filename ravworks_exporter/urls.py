from django.urls import path

from . import views

app_name = 'ravworks_exporter'

urlpatterns = [
    path('', views.index, name='index'),
]
