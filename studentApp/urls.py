from django.urls import path

from . import views

app_name = 'studentApp'
urlpatterns = [
    path('teacher/center/', views.show_teacher, name='TeacherCenter'),
    path('login/', views.login, name='StudentLogin'),
    path('enroll/', views.enroll, name='StudentEnroll'),
    path('create/image/code/', views.create_img_code, name='CreateImgCode'),
    path('person/info/', views.show_info, name='PersonInfo'),
    path('change/code/', views.chang_code, name='ChangeCode'),
    path('logout/', views.logout, name='Logout'),
    path('my/classmates/', views.show_classmates, name='MyClassmates')
]
