from django import forms
from django.contrib.auth.models import User
import re

class FormDangKy(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField()
    password_confirm = forms.CharField()

    def clean_password2(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            password_confirm = self.cleaned_data['password_confirm']

            if password == password_confirm:
                return password_confirm

        raise forms.ValidationError('Mật khẩu không hợp lệ.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Tên tài khoản có ký tự đặc biệt.')
        
        try:
            User.objects.get(username = username)
        except User.DoesNotExist:
            return username
        
        raise forms.ValidationError('Tài khoản đã tồn tại.')

    def save(self):
        User.objects.create_user(username = self.cleaned_data['username'],
                                    email = self.cleaned_data['email'],
                                    password = self.cleaned_data['password'])