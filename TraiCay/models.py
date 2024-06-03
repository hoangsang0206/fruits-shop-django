from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Loai(models.Model):
    MaLoai = models.CharField(max_length=10, primary_key=True)
    TenLoai = models.CharField(max_length=100)

class SanPham(models.Model):
    MaSP = models.CharField(max_length=10, primary_key=True)
    MaLoai = models.ForeignKey(Loai, on_delete=models.SET_NULL, null=True)
    TenSP = models.CharField(max_length=100)
    DonGia = models.DecimalField(max_digits=10, decimal_places=2)
    MoTa = models.TextField()

    def HinhAnh(self):
        hinhanhsp = self.hinhanhsp_set.first()
        return hinhanhsp.HinhAnh if hinhanhsp else None

    def TatCaHinhAnh(self):
        return self.hinhanhsp_set.all()

    def TonKho(self):
        return sum([chitiet.SoLuongTon for chitiet in self.chitietkho_set.all()])

class HinhAnhSP(models.Model):
    SanPham = models.ForeignKey(SanPham, on_delete=models.SET_NULL, null=True)
    HinhAnh = models.TextField()

class KhachHang(models.Model):
    MaKH = models.CharField(max_length=10, primary_key=True)
    TenKH = models.CharField(max_length=100)
    SDT = models.CharField(max_length=20)
    Email = models.CharField(max_length=100)
    DiaChi = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

class NhanVien(models.Model):
    MaNV = models.CharField(max_length=10, primary_key=True)
    TenNV = models.CharField(max_length=100)
    SDT = models.CharField(max_length=20)
    Email = models.CharField(max_length=100)
    DiaChi = models.CharField(max_length=100)

class NhaCungCap(models.Model):
    MaNCC = models.CharField(max_length=10, primary_key=True)
    TenNCC = models.CharField(max_length=100)
    DiaChi = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    SDT = models.CharField(max_length=20)

class HoaDon(models.Model):
    MaHD = models.CharField(max_length=10, primary_key=True)
    MaKH = models.ForeignKey(KhachHang, on_delete=models.SET_NULL, null=True)
    NgayMua = models.DateField()
    TongTien = models.DecimalField(max_digits=10, decimal_places=2),
    DiaChiGiao = models.CharField(max_length=100, null=True),
    PhuongThucThanhToan = models.CharField(max_length=10, null=True),
    TrangThai = models.CharField(max_length=100, null=True)

class ChiTietHoaDon(models.Model):
    MaHD = models.ForeignKey(HoaDon, on_delete=models.SET_NULL, null=True)
    MaSP = models.ForeignKey(SanPham, on_delete=models.SET_NULL, null=True)
    SoLuong = models.IntegerField(default=0)
    DonGia = models.DecimalField(max_digits=10, decimal_places=2)

class Kho(models.Model):
    MaKho = models.CharField(max_length=10, primary_key=True)
    TenKho = models.CharField(max_length=100)
    DiaChiKho = models.CharField(max_length=100)
    SDT = models.CharField(max_length=20)

class ChiTietKho(models.Model):
    MaKho = models.ForeignKey(Kho, on_delete=models.SET_NULL, null=True)
    MaSP = models.ForeignKey(SanPham, on_delete=models.SET_NULL, null=True)
    SoLuongTon = models.IntegerField(default=0)
    NgayHetHan = models.DateField()

class PhieuNhapHang(models.Model):
    MaPNH = models.CharField(max_length=10, primary_key=True)
    MaNCC = models.ForeignKey(KhachHang, on_delete=models.SET_NULL, null=True)
    NgayNhap = models.DateField()
    TongTien = models.DecimalField(max_digits=10, decimal_places=2)

class ChiTietPhieuNhap(models.Model):
    MaPNH = models.ForeignKey(PhieuNhapHang, on_delete=models.SET_NULL, null=True)
    MaSP = models.ForeignKey(SanPham, on_delete=models.SET_NULL, null=True)
    DonGia = models.DecimalField(max_digits=10, decimal_places=2)

class Slider(models.Model):
    HinhAnh = models.TextField()
    Link = models.TextField()

class GioHang(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    SanPham = models.ForeignKey(SanPham, on_delete=models.CASCADE, null=False)
    SoLuong = models.IntegerField(default=0, null=False)