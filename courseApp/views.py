from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from SelectCourses.MyFunction.search import search
from courseApp import models
from studentApp.models import Student


# Create your views here.
# 进行分页
def show_course(request):
    search_courses_obj = search(request)
    if search_courses_obj:
        page_obj = Paginator(search_courses_obj, 10)
    else:
        courses_obj = models.Course.objects.all()
        page_obj = Paginator(courses_obj, 10)
    pagenum = request.GET.get('pagenum', 1)
    current_page = page_obj.get_page(pagenum)
    page_range = range(1, page_obj.num_pages + 1)
    # 判断是否登录
    if request.session.get('student_id'):
        student_obj = Student.objects.get(id=request.session.get('student_id'))
        selected_courses = student_obj.course.all()
        selected_courses_num = selected_courses.all().count()
        return render(request, 'course.html', {'current_page': current_page,
                                               'page_range': page_range,
                                               'selected_courses': selected_courses,
                                               'selected_courses_num': selected_courses_num})
    else:
        return render(request, 'course.html', {'current_page': current_page, 'page_range': page_range})


# 学生选课退课
def select_course(request):
    student_obj = Student.objects.get(id=request.session.get('student_id'))
    course_obj = models.Course.objects.get(id=request.GET.get('course_id'))
    # 判断该课程是否在学生的课程集中
    if course_obj in student_obj.course.all():
        student_obj.course.remove(course_obj)
        print(student_obj.name, course_obj.name, '退课成功')
    else:
        if student_obj.course.all().count() < 5:
            student_obj.course.add(course_obj)
            print(student_obj.name, course_obj.name, '选课成功')
        else:
            return redirect(reverse('courseApp:CourseCenter'))
    return redirect(reverse('courseApp:CourseCenter'))
