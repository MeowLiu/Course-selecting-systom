# Generated by Django 4.1.7 on 2023-06-07 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacherApp', '0003_teacher_gender_alter_teacher_age_alter_teacher_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='introduce',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='简介'),
        ),
    ]
