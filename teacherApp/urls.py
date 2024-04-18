from django.urls import path

from . import views

app_name = 'teacherApp'
urlpatterns = [
    path('teacher/home',views.go_home,name='GoHome'),
    path('student/center', views.show_student, name='StudentCenter'),
    path('login/', views.login, name='TeacherLogin'),
    path('enroll/', views.enroll, name='TeacherEnroll'),
    path('create/image/code/', views.create_img_code, name='CreateImgCode'),
    path('person/info/', views.show_info, name='PersonInfo'),
    # path('teach/course/', views.my_course, name='TeachCourse'),
    path('change/code/', views.chang_code, name='ChangeCode'),
    path('logout/', views.logout, name='Logout')
]
