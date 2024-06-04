from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

import json

from .models import *
from .forms import FormDangKy

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import LoaiSerializer, SanPhamSerializer

# Create your views here.
def dangky(request):
    form = FormDangKy
    if request.method == 'POST':
        form = FormDangKy(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')

    return render(request, 'dangky.html', {'form': form})

def home(request):
    Home_Fruits = []
    DSLoai = Loai.objects.all()[:7]
    for loai in DSLoai:
        sanpham = SanPham.objects.filter(MaLoai = loai)
        fruits = {'loai': loai, 'fruits': sanpham}
        Home_Fruits.append(fruits)

    Sliders = Slider.objects.all()

    return render(request, 'home.html', {'Home_Fruits' : Home_Fruits, 'Sliders': Sliders})

def loc_theo_loai(request, id):
    loai = None
    if id == 'all':
        sanpham = SanPham.objects.all()
    else:
        loai = get_object_or_404(Loai, pk=id)
        sanpham = SanPham.objects.filter(MaLoai = loai)

    # phân trang
    limit = 20
    page = request.GET.get('page', 1)

    sanpham_paginator = Paginator(sanpham, limit)
    try:
        sanpham_page = sanpham_paginator.get_page(page)
    except PageNotAnInteger:
        sanpham_page = sanpham_paginator.get_page(1)
    except EmtyPage:
        sanpham_page = sanpham_paginator.get_page(sanpham_paginator.num_pages)

    current_page = sanpham_page.number
    num_pages = sanpham_paginator.num_pages
    page_range = sanpham_paginator.page_range
    previous_page = current_page - 1
    next_page = current_page + 1
    start_page = current_page - 1 if current_page > 1 else 1
    end_page = current_page + 1 if current_page < num_pages else num_pages

    context = {
        'Fruits': sanpham_page,
        'current_page': current_page,
        'num_pages': num_pages,
        'page_range': page_range,
        'previous_page': previous_page,
        'next_page': next_page,
        'start_page': start_page,
        'end_page': end_page,
        'Loai': loai
    }

    return render(request, 'loai.html', context)

def tim_kiem(request):
    query = request.GET.get('q')
    if query:
        sanpham = SanPham.objects.filter(TenSP__icontains=query)
    else:
        sanpham = SanPham.objects.all()

    # phân trang
    limit = 20
    page = request.GET.get('page', 1)

    sanpham_paginator = Paginator(sanpham, limit)
    try:
        sanpham_page = sanpham_paginator.get_page(page)
    except PageNotAnInteger:
        sanpham_page = sanpham_paginator.get_page(1)
    except EmtyPage:
        sanpham_page = sanpham_paginator.get_page(sanpham_paginator.num_pages)

    current_page = sanpham_page.number
    num_pages = sanpham_paginator.num_pages
    page_range = sanpham_paginator.page_range
    previous_page = current_page - 1
    next_page = current_page + 1
    start_page = current_page - 1 if current_page > 1 else 1
    end_page = current_page + 1 if current_page < num_pages else num_pages

    context = {
        'value': query,
        'Fruits': sanpham_page,
        'current_page': current_page,
        'num_pages': num_pages,
        'page_range': page_range,
        'previous_page': previous_page,
        'next_page': next_page,
        'start_page': start_page,
        'end_page': end_page,
    }

    return render(request, 'timkiem.html', context)

def sanpham(request, id):
    sanpham = get_object_or_404(SanPham,  pk=id)
    loai = sanpham.MaLoai
    spkho = ChiTietKho.objects.filter(MaSP=sanpham)

    return render(request, 'sanpham.html', {'Loai': loai, 'Fruit': sanpham})

def giohang(request):
    user = request.user
    if user and user.is_authenticated:
        giohang = GioHang.objects.filter(user = user)
        for gh in giohang:
            if gh.SanPham.TonKho() <= 0:
                gh.delete()

        giohang = GioHang.objects.filter(user = user)
        total = sum([gh.SanPham.DonGia * gh.SoLuong for gh in giohang])
        return render(request, 'giohang.html', {'Cart': giohang, 'TongTien': total})
    else:
        session_cart = request.session.get('cart', None)
        cart = []
        total = 0
        if session_cart:
            for c in session_cart:
                sanpham = get_object_or_404(SanPham, pk=c['MaSP'])
                if sanpham.TonKho() <= 0:
                    session_cart.remove(c)
                    request.session['cart'] = session_cart
                else:
                    total += sanpham.DonGia * c['SoLuong']
                    cart.append({'SanPham': sanpham, 'SoLuong': c['SoLuong']})
            return render(request, 'giohang.html', {'Cart': cart, 'TongTien': total})

    return render(request, 'giohang.html')

def taikhoan(request):
    user = request.user
    if not user or not user.is_authenticated:
        return HttpResponseRedirect('/dangnhap')

    try:
        kh = KhachHang.objects.get(user=user)
        return render(request, 'taikhoan.html', {'KH': kh})
    except Exception:
        pass
    return render(request, 'taikhoan.html')
    
### API ###################################################################################
@api_view(['GET'])
def getLoai(request):
    loai = Loai.objects.all()
    return Response(LoaiSerializer(loai, many=True).data)

@api_view(['GET'])
def getTimKiem(request):
    query = request.GET.get('q')
    if query:
        sanpham = SanPham.objects.filter(TenSP__icontains=query)
    else:
        sanpham = SanPham.objects.all()
    
    serializer = SanPhamSerializer(sanpham, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_so_luong(request):
    tong = 0

    user = request.user
    if user and user.is_authenticated:
        giohang = GioHang.objects.filter(user=user)
        tong = len(giohang)
    else:
        session_cart = request.session.get('cart', [])
        tong = len(session_cart)
    return Response({'tong': tong}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def them_gio_hang(request):
    msp = request.data.get('id')
    sanpham = get_object_or_404(SanPham, pk=msp)
    if sanpham.TonKho() <= 0:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    user = request.user
    if user and user.is_authenticated:
        try:
            giohang = GioHang.objects.get(user=user, SanPham=sanpham)
            giohang.SoLuong += 1
            giohang.save()
        except GioHang.DoesNotExist:
            GioHang.objects.create(user=user, SanPham=sanpham, SoLuong=1)
    else:
        is_exist = False
        session_cart = request.session.get('cart', [])
        if session_cart:
            for c in session_cart:
                if c['MaSP'] == sanpham.MaSP:
                    c['SoLuong'] += 1
                    is_exist = True
                    break
        
        if not is_exist:
            if not session_cart:
                session_cart = []

            session_cart.append({'MaSP': sanpham.MaSP, 'SoLuong': 1})

        request.session['cart'] = session_cart

    return Response(status=status.HTTP_200_OK)

@api_view(['DELETE'])
def xoa_sanpham_gio_hang(request):
    msp = request.data.get('id')
    sanpham = get_object_or_404(SanPham, pk=msp)

    user = request.user
    if user and user.is_authenticated:
        giohang = GioHang.objects.get(user=user, SanPham=sanpham)
        if giohang:
            giohang.delete()
    else:
        session_cart = request.session.get('cart', [])
        if session_cart:
            for c in session_cart:
                if c['MaSP'] == sanpham.MaSP:
                    session_cart.remove(c)
                    request.session['cart'] = session_cart
                    break

    return Response(status=status.HTTP_200_OK)

@api_view(['PUT'])
def cap_nhat_so_luong(request):
    msp = request.data.get('id')
    sanpham = get_object_or_404(SanPham, pk=msp)
    update_type = request.data.get('type')
    user = request.user

    total_price = 0
    res_qty = 0

    if update_type:
        if user and user.is_authenticated:
            giohang = GioHang.objects.get(user=user, SanPham=sanpham)
            if giohang:
                if update_type == 'increase':
                    giohang.SoLuong += 1
                    if sanpham.TonKho() < giohang.SoLuong:
                        giohang.SoLuong = sanpham.TonKho()
                else:
                    giohang.SoLuong -= 1
                    if giohang.SoLuong <= 0:
                        giohang.SoLuong = 1
                res_qty = giohang.SoLuong
                giohang.save()

        else:
            session_cart = request.session.get('cart', [])
            if session_cart:
                for c in session_cart:
                    if c['MaSP'] == sanpham.MaSP:
                        if update_type == 'increase':
                            c['SoLuong'] += 1
                            if sanpham.TonKho() < c['SoLuong']:
                                c['SoLuong'] = sanpham.TonKho()
                        else:
                            c['SoLuong'] -= 1
                            if c['SoLuong'] == 0:
                                c['SoLuong']= 1
                        request.session['cart'] = session_cart
                        res_qty = c['SoLuong']
                        break
                    

    else:
        qty = request.data.get('qty')
        qty = float(qty)

        if user and user.is_authenticated:
            giohang = GioHang.objects.get(user=user, SanPham=sanpham)
            if giohang:
                if sanpham.TonKho() >= qty:
                    giohang.SoLuong = qty
                else:
                    giohang.SoLuong = sanpham.TonKho()

                if giohang.SoLuong <= 0:
                    giohang.SoLuong = 1
                giohang.save()
                res_qty = giohang.SoLuong

        else:
            session_cart = request.session.get('cart', [])
            if session_cart:
                for c in session_cart:
                    if c['MaSP'] == sanpham.MaSP:
                        if sanpham.TonKho() >= qty:
                            c['SoLuong'] = qty
                        else:
                            c['SoLuong'] = sanpham.TonKho()
                        if c['SoLuong'] <= 0:
                            c['SoLuong'] = 1
                        request.session['cart'] = session_cart
                        res_qty = c['SoLuong']
                        break

    if user and user.is_authenticated:
        giohang = GioHang.objects.filter(user=user)
        total_price = sum(gh.SoLuong * gh.SanPham.DonGia for gh in giohang)
    else:
        session_cart = request.session.get('cart', [])
        for c in session_cart:
            sp = get_object_or_404(SanPham, pk=c['MaSP'])
            total_price += sp.DonGia * c['SoLuong']

    return Response({'total': total_price, 'qty': res_qty}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def doi_mat_khau(request):
    user =request.user
    if not user or not user.is_authenticated:
        return Response(status=status.HTTP_403_FORBIDDEN)

    old_p = request.data.get('old_p')
    new_p = request.data.get('new_p')
    conf_p = request.data.get('confirm_p')

    if not user.check_password(old_p):
        return Response({'success': False, 'error': 'Mật khẩu cũ không đúng'}, status=status.HTTP_200_OK)
    if new_p != conf_p:
        return Response({'success': False, 'error': 'Xác nhận mật khẩu không đúng'}, status=status.HTTP_200_OK)
    
    user.set_password(new_p)
    user.save()
    update_session_auth_hash(request, user)

    return Response({'success': True}, status=status.HTTP_200_OK)

@api_view(['PUT'])
def sua_thong_tin_kh(request):
    user = request.user
    if not user or not user.is_authenticated:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    fullname = request.data.get('fullname')
    phone = request.data.get('phone')
    email = request.data.get('email')
    address = request.data.get('address')

    try:
        kh = KhachHang.objects.get(user=user)
        kh.TenKH = fullname
        kh.SDT = phone
        kh.Email = email
        kh.DiaChi = address
        kh.save()

        user.email = email
        user.save()
        update_session_auth_hash(request, user)

        return Response({'success': True}, status=status.HTTP_200_OK)
    except KhachHang.DoesNotExist:

        KhachHang.objects.create(MaKH=random_makh(), TenKH=fullname, SDT=phone, Email=email, DiaChi=address, user=user)
        return Response({'success': True}, status=status.HTTP_200_OK)
    except Exception:
        pass

    return Response(status=status.HTTP_403_FORBIDDEN)




def random_makh():
    all_kh = KhachHang.objects.order_by('MaKH')
    
    if all_kh:
        last_kh = all_kh.last()
        num = int(last_kh.MaKH[2:])
        return 'KH{:06d}'.format(num + 1)

    return 'KH000001'