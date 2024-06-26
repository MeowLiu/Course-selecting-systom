# Generated by Django 4.1.7 on 2023-06-05 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courseApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.CharField(max_length=12, primary_key=True, serialize=False, verbose_name='教师编号')),
                ('acount_name', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=12, verbose_name='密码')),
                ('name', models.CharField(max_length=32, verbose_name='教师姓名')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('course', models.ManyToManyField(to='courseApp.course', verbose_name='所授课程')),
            ],
        ),
    ]
