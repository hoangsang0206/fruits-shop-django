from django import forms
from django.contrib.auth.models import User
import re
from .models import *

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









class ThemLoaiForm(forms.Form):
    MaLoai = forms.CharField(label='Mã loại', max_length=100)
    TenLoai = forms.CharField(label='Tên loại', max_length=100)

    def clean_TenLoai(self):
        MaLoai = self.cleaned_data['MaLoai']
        TenLoai = self.cleaned_data['TenLoai']
        if Loai.objects.filter(MaLoai=MaLoai).exists():
            raise forms.ValidationError("Mã loại đã tồn tại")
        if Loai.objects.filter(TenLoai=TenLoai).exists():
            raise forms.ValidationError("Tên loại đã tồn tại")
        return TenLoai

    def save(self):
        loai = Loai(
            MaLoai=self.cleaned_data['MaLoai'],
            TenLoai=self.cleaned_data['TenLoai']
        )
        loai.save()

class XoaLoaiForm(forms.Form):
    MaLoai = forms.CharField(label='Mã loại', max_length=100)

    def clean_MaLoai(self):
        MaLoai = self.cleaned_data['MaLoai']
        if not Loai.objects.filter(MaLoai=MaLoai).exists():
            raise forms.ValidationError("Mã loại không tồn tại")
        return MaLoai

    def delete(self):
        MaLoai = self.cleaned_data['MaLoai']
        Loai.objects.filter(MaLoai=MaLoai).delete()

class SuaLoaiForm(forms.Form):
    MaLoai = forms.CharField(label='Mã loại', max_length=100)
    TenLoai = forms.CharField(label='Tên loại', max_length=100)
   
    def clean_TenLoai(self):
        TenLoai = self.cleaned_data['TenLoai']
        if Loai.objects.filter(TenLoai=TenLoai).exists():
            raise forms.ValidationError("Tên loại đã tồn tại")
        return TenLoai
    
    def save(self):
        MaLoai = self.cleaned_data['MaLoai']
        TenLoai = self.cleaned_data['TenLoai']
        loai = Loai.objects.get(MaLoai=MaLoai)
        loai.TenLoai = TenLoai
        loai.save()

class ThemSPForm(forms.Form):
    MaSP = forms.CharField(label='Mã sản phẩm', max_length=100)
    MaLoai = forms.CharField(label='Loại', max_length=100)
    TenSP = forms.CharField(label='Tên sản phẩm', max_length=100)
    DonGia = forms.DecimalField(label='Đơn giá', max_digits=10, decimal_places=2)
    MoTa = forms.CharField(label='Mô tả', max_length=100)

    def clean_MaSP(self):
        MaSP = self.cleaned_data['MaSP']
        if SanPham.objects.filter(MaSP=MaSP).exists():
            raise forms.ValidationError("Mã sản phẩm đã tồn tại!")
        return MaSP

    def clean_MaLoai(self):
        MaLoai = self.cleaned_data['MaLoai']
        if not Loai.objects.filter(MaLoai=MaLoai).exists():  
            raise forms.ValidationError("Mã loại không tồn tại")
        return MaLoai

    def clean_TenSP(self):
        TenSP = self.cleaned_data['TenSP']
        if SanPham.objects.filter(TenSP=TenSP).exists():
            raise forms.ValidationError("Tên sản phẩm đã tồn tại!")
        return TenSP
        
    def clean_DonGia(self):
        DonGia = self.cleaned_data['DonGia']
        if DonGia < 0:
            raise forms.ValidationError("Giá tiền không được nhỏ hơn 0!")
        return DonGia

    def save(self):
        sanpham = SanPham(
            MaSP=self.cleaned_data['MaSP'],
            MaLoai=Loai.objects.get(MaLoai=self.cleaned_data['MaLoai']),
            TenSP=self.cleaned_data['TenSP'],
            DonGia=self.cleaned_data['DonGia'],
            MoTa=self.cleaned_data['MoTa'],
        )
        sanpham.save()

class XoaSPForm(forms.Form):
    MaSP = forms.CharField(label='Mã sản phẩm', max_length=100)

    def clean_MaLoai(self):
        MaSP = self.cleaned_data['MaSP']
        if not SanPham.objects.filter(MaSP=MaSP).exists():
            raise forms.ValidationError("Mã sản phẩm không tồn tại")
        return MaSP

    def delete(self):
        MaSP = self.cleaned_data['MaSP']
        SanPham.objects.filter(MaSP=MaSP).delete()

class SuaSPForm(forms.Form):
    MaSP = forms.CharField(label='Mã sản phẩm', max_length=100)
    MaLoai = forms.CharField(label='Loại', max_length=100)
    TenSP = forms.CharField(label='Tên sản phẩm', max_length=100)
    DonGia = forms.DecimalField(label='Đơn giá', max_digits=10, decimal_places=2)
    MoTa = forms.CharField(label='Mô tả', max_length=100)
   
    def clean_TenSP(self):
        TenSP = self.cleaned_data['TenSP']
        if SanPham.objects.filter(TenSP=TenSP).exists():
            raise forms.ValidationError("Tên loại đã tồn tại")
        return TenSP
    
    def clean_DonGia(self):
        DonGia = self.cleaned_data['DonGia']
        if DonGia < 0:
            raise forms.ValidationError("Giá tiền không được nhỏ hơn 0!")
        return DonGia
    
    def save(self):
        sanpham = SanPham(
            MaSP=self.cleaned_data['MaSP'],
            MaLoai=Loai.objects.get(MaLoai=self.cleaned_data['MaLoai']),
            TenSP=self.cleaned_data['TenSP'],
            DonGia=self.cleaned_data['DonGia'],
            MoTa=self.cleaned_data['MoTa'],
        )
        sanpham.save()