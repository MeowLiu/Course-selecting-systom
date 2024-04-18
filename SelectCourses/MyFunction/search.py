from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse

from courseApp.models import Course
from studentApp.models import Student
from teacherApp.models import Teacher


# 自定义搜索函数
def search(request, selected_courses=None):
    if request.method == 'POST':
        search_content = request.POST.get('search')
        if 'course/center/' in request.path_info:
            search_courses_obj = Course.objects.filter(
                Q(id__contains=search_content) |
                Q(name__contains=search_content) |
                Q(place__contains=search_content) |
                Q(time__contains=search_content) |
                Q(teacher__name__contains=search_content))
            return search_courses_obj
        elif 'teacher/center/' in request.path_info:
            search_teachers_obj = Teacher.objects.filter(name__contains=search_content)
            return search_teachers_obj
        elif 'my/classmates/' in request.path_info:
            search_my_classmates = []
            student_obj = Student.objects.get(id=request.session.get('student_id'))
            for course in selected_courses:
                # 模糊查询，去掉自身信息，得到列表
                classmates = course.student_set.filter(
                    Q(name__contains=search_content) |
                    Q(id__contians=search_content) |
                    Q(course__contians=search_content)
                ).exclude(id=student_obj.id)
                search_my_classmates += classmates
            return search_my_classmates
        else:
            print('我重定向啦')
            return redirect(reverse('homeApp:Home'))
    else:
        return None
