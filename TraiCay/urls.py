from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='TrangChu'),
    path('dangnhap/', auth_views.LoginView.as_view(template_name='dangnhap.html', next_page='/'), name='DangNhap'),
    path('dangxuat/', auth_views.LogoutView.as_view(next_page='/'), name='DangXuat'),
    path('dangky/', views.dangky, name='DangKy'),
    path('home/', views.home, name='TrangChu'),
    path('loai/<str:id>', views.loc_theo_loai, name='LocTheoLoai'),
    path('timkiem/', views.tim_kiem, name='TimKiem'),
    path('sanpham/<str:id>', views.sanpham, name='SanPham'),
    path('giohang/', views.giohang, name='GioHang'),
    path('taikhoan/', views.taikhoan, name='TaiKhoan'),
    path('dathang/kiemtra', views.kiem_tra_thong_tin_dat_hang, name='KiemTraTTDatHang'),
    path('dathang/chitiet', views.tt_dat_hang, name='TTDatHang'),
    path('dathang/thanhtoan', views.thanh_toan, name='ThanhToan'),
    path('dathang/thanhcong', views.thanh_toan_thanh_cong, name='TToanThanhCong'),
    path('dathang/thatbai', views.thanh_toan_that_bai, name='TToanThatBai'),

    path('api/loai/', views.getLoai, name='GetLoai'),
    path('api/timkiem/', views.getTimKiem, name='GetTimKiem'),
    path('api/giohang/them', views.them_gio_hang, name='ThemGioHang'),
    path('api/giohang/capnhat', views.get_so_luong, name='GetSoLuong'),
    path('api/giohang/xoa', views.xoa_sanpham_gio_hang, name='XoaGioHang'),
    path('api/giohang/capnhatsoluong', views.cap_nhat_so_luong, name='CapNhatSoLuong'),
    path('api/taikhoan/doimatkhau', views.doi_mat_khau, name='DoiMatKhau'),
    path('api/taikhoan/capnhat', views.sua_thong_tin_kh, name='SuaThongTin'),
    path('api/donhang/timkiem', views.get_hoa_don, name='TimHoaDon'),
]