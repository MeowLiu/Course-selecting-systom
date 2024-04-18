from django import forms
from django.forms import ModelForm

from teacherApp import models


class LoginModelform(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='密码')
    validcode = forms.CharField(widget=forms.TextInput, label='验证码')

    class Meta:
        model = models.Teacher
        fields = ['acount_name', 'password', 'validcode']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': '请输入' + field.label}
            field.error_messages = {'required': '内容不能为空哦', 'max_length': '长度超出啦！'}


# 教师注册模型表单
class EnrollModelForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=12, label='密码')

    class Meta:
        model = models.Teacher
        fields = ['id', 'acount_name', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.error_messages = {'required': '内容不能为空哦', 'max_length': '长度超出啦！'}
            if field_name == 'id':
                field.widget.attrs = {'class': 'form-control', 'placeholder': '请设置' + field.label}
            else:
                field.widget.attrs = {'class': 'form-control', 'placeholder': '请输入' + field.label}
