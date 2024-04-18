from django.db import models

from courseApp.models import Course


# Create your models here.

# 学生表
class Student(models.Model):
    id = models.CharField(max_length=12, primary_key=True, verbose_name='学号')
    acount_name = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=12, verbose_name='密码')
    name = models.CharField(max_length=32, verbose_name='学生姓名', blank=True, null=True)
    age = models.CharField(verbose_name='年龄', max_length=32, blank=True, null=True)
    # gender_choice = ((1, '男'), (2, '女'), (3, '未知'))
    gender = models.CharField(max_length=32, verbose_name='性别', blank=True, null=True)
    place = models.CharField(max_length=32, verbose_name='所在地', blank=True, null=True)

    course = models.ManyToManyField(Course, verbose_name='已选课程')

    def __str__(self):
        return f'姓名：{self.name}'
