from django.db import models

from teacherApp.models import Teacher


# Create your models here.


# 课表
class Course(models.Model):
    id = models.CharField(max_length=6, primary_key=True, verbose_name="课程编号")
    name = models.CharField(max_length=32, verbose_name="课程名称")
    credits = models.SmallIntegerField(verbose_name="课程学分", default=2)
    place = models.CharField(max_length=32, verbose_name="上课地点")
    time = models.CharField(max_length=32, verbose_name="上课时间")
    # teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='任课老师')
    introduction = models.TextField(verbose_name="书籍详情", default="xxx")

    def __str__(self):
        return f"课程名称：{self.name}"
