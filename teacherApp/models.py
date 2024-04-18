from django.db import models


# Create your models here.
# 教师表
class Teacher(models.Model):
    id = models.CharField(max_length=12, primary_key=True, verbose_name='教师编号')
    acount_name = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=12, verbose_name='密码')
    name = models.CharField(max_length=32, verbose_name='教师姓名', blank=True, null=True)
    age = models.IntegerField(verbose_name='年龄', blank=True, null=True)
    gender_choice = ((1, '男'), (2, '女'), (3, '未知'))

    gender = models.SmallIntegerField(choices=gender_choice, verbose_name='性别', blank=True, null=True)
    introduce = models.TextField(verbose_name='简介', max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name