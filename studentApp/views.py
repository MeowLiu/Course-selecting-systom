from io import BytesIO

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse

from SelectCourses.MyFunction.imagecode import create_imgcode
from SelectCourses.MyFunction.search import search
from studentApp import models
from studentApp.StudentModelForm import LoginModelForm, EnrollModelForm, ChangeCode
from teacherApp.models import Teacher


# Create your views here.


# 展示老师信息
def show_teacher(request):
    search_teachers_obj = search(request)
    if search_teachers_obj:
        page_obj = Paginator(search_teachers_obj, 3)
    else:
        teachers_obj = Teacher.objects.all()
        page_obj = Paginator(teachers_obj, 3)
    pagenum = request.GET.get('pagenum', 1)
    current_page = page_obj.get_page(pagenum)
    page_range = range(1, page_obj.num_pages + 1)
    return render(request, 'teacher.html', {'current_page': current_page, 'page_range': page_range})


# 创建带有随机验证码的图片
def create_img_code(request):
    img, validcode = create_imgcode()
    request.session['validcode'] = validcode
    request.session.set_expiry(60)
    io_stream = BytesIO()
    img.save(io_stream, format='png')
    return HttpResponse(io_stream.getvalue())


# 使用模型表单进行学生登录
def login(request):
    if request.method == 'GET':
        # 创建空表单
        form = LoginModelForm()
        return render(request, 'slogin.html', {'form': form})
    elif request.method == 'POST':
        # 进行校验
        form = LoginModelForm(request.POST)
        if form.is_valid():
            validcode = form.cleaned_data.pop('validcode')
            if validcode.lower() != request.session.get('validcode', '').lower():
                prompt = '验证码错误!'
                return render(request, 'slogin.html', {'prompt': prompt, 'form': form})
            original_student = models.Student.objects.filter(**form.cleaned_data)
            if original_student.exists():
                request.session['student_name'] = original_student.first().name
                request.session['student_id'] = original_student.first().id

                del request.session['validcode']
                request.session.set_expiry(60 * 60 * 24 * 7)
                print(request.session.get('student_name'), '登录啦')
                # 这里应该使用反向解析回到学生专属home
                return redirect('homeApp:Home')
            else:
                prompt = '账号或密码错误！'
                return render(request, 'slogin.html', {'form': form, 'prompt': prompt})
        else:
            return render(request, 'slogin.html', {'form': form})


# 使用模型表单进行学生注册
def enroll(request):
    if request.method == 'GET':
        form = EnrollModelForm()
        return render(request, 'senroll.html', {'form': form})
    elif request.method == 'POST':
        sid = request.POST.get('id')
        acount_name = request.POST.get('acount_name')
        form = EnrollModelForm(request.POST)
        if form.is_valid():
            original_student = models.Student.objects.filter(Q(id=sid) | Q(acount_name=acount_name))
            if not original_student.exists():
                form.save()
                # 我应该在这里写一个注册成功的页面
                return render(request, 'home.html')
            else:
                prompt = '学号或用户名已存在，请更换后重试~'
                return render(request, 'senroll.html', {'form': form, 'prompt': prompt})
        else:
            return render(request, 'senroll.html', {'form': form})


# 学生登录后展示学生个人信息
def show_info(request):
    print(request.session.get('student_name'), '在查看个人信息')
    # 通过session获取学生对象
    sid = request.session['student_id']
    student_obj = models.Student.objects.filter(id=sid).first()
    if request.method == 'POST':
        print(request.session.get('student_name'), '修改了个人信息')
        new_info = request.POST
        # 进行数据更新
        models.Student.objects.filter(id=sid).update(
            acount_name=new_info.get('new_acount_name'),
            age=new_info.get('new_age'),
            gender=new_info.get('new_gender'),
            place=new_info.get('new_place')
        )
        return redirect(reverse('studentApp:PersonInfo'))
    else:
        return render(request, 'student_info.html', {'student_obj': student_obj})


# 学生登录之后修改密码
def chang_code(request):
    print(request.session.get('student_name'), '在修改密码')
    student_obj = models.Student.objects.get(id=request.session.get('student_id'))
    if request.method == 'GET':
        # 创建空表单
        form = ChangeCode()
        return render(request, 'change_code.html', {'form': form})
    elif request.method == 'POST':
        # 进行字段绑定
        form = ChangeCode(request.POST, instance=student_obj)
        if form.is_valid():
            old_password = form.cleaned_data.pop('old_password')
            confirm_password = form.cleaned_data.pop('confirm_password')
            password = form.cleaned_data.get('password')
            if models.Student.objects.filter(id=student_obj.id, password=old_password).exists():
                if confirm_password != password:
                    prompt = '两次新密码不一致哦'
                    return render(request, 'change_code.html', {'form': form, 'prompt': prompt})
                elif password == old_password:
                    prompt = '新密码不能与原密码相同哦'
                    return render(request, 'change_code.html', {'form': form, 'prompt': prompt})
                else:
                    # 保存密码并重定向至学生登录界面
                    form.save()
                    return redirect(reverse('studentApp:StudentLogin'))
            else:
                prompt = '原密码错误！'
                return render(request, 'change_code.html', {'form': form, 'prompt': prompt})
        else:
            return render(request, 'change_code.html', {'form': form})


# 退出登录
def logout(request):
    print(request.session.get('student_name'), '退出登录啦')
    request.session.clear()
    return redirect(reverse('homeApp:Home'))


# 展示我的同学
def show_classmates(request):
    print(request.session.get('student_name'), '在查看自己的同学')
    my_classmates = []
    student_obj = models.Student.objects.get(id=request.session.get('student_id'))
    selected_courses = student_obj.course.all()
    for course in selected_courses:
        # 多对多关系，循环找与我同课的同学
        classmates = course.student_set.all().exclude(id=student_obj.id)  # 去掉自身的信息，得到查询集
        my_classmates += classmates
    search_my_classmates = search(request, selected_courses)
    # 分页
    if search_my_classmates:
        # 如果有进行查询，对同学去重
        search_my_classmates = list(set(search_my_classmates))
        page_obj = Paginator(search_my_classmates, 10)
    else:
        # 没进行查询，对同学去重
        my_classmates = list(set(my_classmates))
        page_obj = Paginator(my_classmates, 10)
    pagenum = request.GET.get('pagenum', 1)
    current_page = page_obj.get_page(pagenum)
    print(current_page)
    page_range = range(1, page_obj.num_pages + 1)
    return render(request, 'my_classmates.html',
                  {'selected_courses': selected_courses, 'current_page': current_page,
                   'page_range': page_range})
