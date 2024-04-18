from django.urls import path

from . import views

app_name = 'courseApp'
urlpatterns = [
    path('center/', views.show_course, name='CourseCenter'),
    path('select/course',views.select_course,name='SelectCourse')
]
