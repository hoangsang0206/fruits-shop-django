from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='TrangChu'),
    path('dangnhap/', auth_views.LoginView.as_view(template_name='dangnhap.html', next_page='/'), name='DangNhap'),
    path('dangxuat/', auth_views.LogoutView.as_view(next_page='/'), name='DangXuat'),
    path('dangky/', views.dangky, name='DangKy'),
    path('home/', views.home, name='TrangChu'),
    path('loai/<str:id>', views.loc_theo_loai, name='LocTheoLoai'),
    path('timkiem/', views.tim_kiem, name='TimKiem'),
    path('sanpham/<str:id>', views.sanpham, name='SanPham'),
    path('giohang', views.giohang, name='GioHang'),

    path('api/loai/', views.getLoai, name='GetLoai'),
    path('api/timkiem/', views.getTimKiem, name='GetTimKiem'),
]