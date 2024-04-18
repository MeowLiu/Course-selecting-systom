from django import forms
from django.forms import ModelForm

from studentApp import models


# 学生登陆模型表单
class LoginModelForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=12, label='密码')

    validcode = forms.CharField(widget=forms.TextInput, label='验证码')

    class Meta:
        model = models.Student
        fields = ['acount_name', 'password', 'validcode']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': '请输入' + field.label}
            field.error_messages = {'required': '内容不能为空哦', 'max_length': '长度超出啦！'}


# 学生注册模型表单
class EnrollModelForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=12, label='密码')

    class Meta:
        model = models.Student
        fields = ['id', 'acount_name', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.error_messages = {'required': '内容不能为空哦', 'max_length': '长度超出啦！'}
            if field_name == 'id':
                field.widget.attrs = {'class': 'form-control', 'placeholder': '请设置' + field.label}
            else:
                field.widget.attrs = {'class': 'form-control', 'placeholder': '请输入' + field.label}


# 学生修改密码模型表单
class ChangeCode(ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput, max_length=12, label='原密码')
    password = forms.CharField(widget=forms.PasswordInput, max_length=12, label='新密码')
    confirm_password = forms.CharField(widget=forms.PasswordInput, max_length=12, label='新密码')

    class Meta:
        model = models.Student
        fields = ['old_password', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.error_messages = {'required': '内容不能为空哦', 'max_length': '长度超出啦！'}
            if field_name == 'old_password':
                field.widget.attrs = {'class': 'form-control', 'placeholder': '请输入' + field.label}
            elif field_name == 'password':
                field.widget.attrs = {'class': 'form-control', 'placeholder': '请设置' + field.label}
            else:
                field.widget.attrs = {'class': 'form-control', 'placeholder': '请再次确认' + field.label}
