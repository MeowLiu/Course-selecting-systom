from django.urls import path

from . import views

app_name = 'homeApp'
urlpatterns = [
    path('', views.home, name='Home'),
]
