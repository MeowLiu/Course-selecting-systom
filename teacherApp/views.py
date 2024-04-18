from io import BytesIO

from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse

from teacherApp import models
from teacherApp.TeacherModelForm import LoginModelform, EnrollModelForm
from teacherApp.imagecode import create_imgcode


# Create your views here.
def go_home(request):
    return render(request, 'teacherhome.html')


def show_student(request):
    return render(request, 'student.html')


# 创建带有随机验证码的图片
def create_img_code(request):
    img, validcode = create_imgcode()
    request.session['validcode'] = validcode
    request.session.set_expiry(60)
    io_stream = BytesIO()
    img.save(io_stream, format='png')
    return HttpResponse(io_stream.getvalue())


# 模型表单进行登录验证
def login(request):
    if request.method == 'GET':
        # 创建空表单
        form = LoginModelform()
        return render(request, 'tlogin.html', {'form': form})
    elif request.method == 'POST':
        # 进行校验
        form = LoginModelform(request.POST)
        if form.is_valid():
            validcode = form.cleaned_data.pop('validcode')
            if validcode.lower() != request.session.get('validcode').lower():
                prompt = '验证码错误!'
                return render(request, 'tlogin.html', {'form': form, 'prompt': prompt})
            oringinal_teacher = models.Teacher.objects.filter(**form.cleaned_data)
            if oringinal_teacher.exists():
                request.session['teacher_name'] = oringinal_teacher.first().name
                del request.session['validcode']
                request.session.set_expiry(60 * 60 * 24 * 7)
                # 反向解析到教师专属home
                return redirect(reverse('home'))
            else:
                prompt = '账号或密码错误！'
                return render(request, 'tlogin.html', {'form': form, 'prompt': prompt})
        else:
            return render(request, 'tlogin.html', {'form': form})


# 使用模型表单进行注册
def enroll(request):
    if request.method == 'GET':
        form = EnrollModelForm()
        return render(request, 'tenroll.html', {'form': form})
    elif request.method == 'POST':
        tid = request.POST.get('id')
        acount_name = request.POST.get('acount_name')
        form = EnrollModelForm(request.POST)
        if form.is_valid():
            original_teacher = models.Teacher.objects.filter(Q(id=tid) | Q(acount_name=acount_name))
            if not original_teacher.exists():
                form.save()
                # 我应该在这里写一个注册成功的页面
                return render(request, 'home.html')
            else:
                prompt = '教师编号或用户名已存在，请更换后重试~'
                return render(request, 'tenroll.html', {'form': form, 'prompt': prompt})
        else:
            return render(request, 'tenroll.html', {'form': form})


def show_info(request):
    return render(request, 'teacher_info.html')


def chang_code(request):
    return render(request, 'change_code.html')


def logout(request):
    request.session.clear()
    return redirect(reverse('home'))

