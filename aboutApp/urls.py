from django.urls import path
from . import views

app_name='aboutApp'

urlpatterns=[
    path('us/',views.show_us,name='Us')
]