# Generated by Django 4.1 on 2024-04-23 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseApp', '0004_remove_course_teacher_course_introduction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='introduction',
            field=models.TextField(default='xxx', verbose_name='书籍详情'),
        ),
    ]
