from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login

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
    images = HinhAnhSP.objects.filter(SanPham = sanpham)
    spkho = ChiTietKho.objects.filter(MaSP=sanpham)
    quantity = 0
    if spkho:
        for spk in spkho:
            quantity += spk.SoLuongTon

    return render(request, 'sanpham.html', {'Loai': loai, 'Fruit': sanpham, 'Quantity': quantity, 'images': images})

def giohang(request):
    user = request.user
    if user and user.is_authenticated:
        giohang = GioHang.objects.filter(user = user)
        return render(request, 'giohang.html', {'Cart': giohang})
    else:
        session_cart = request.session.get('cart', None)
        cart = []
        if session_cart:
            for c in session_cart:
                sanpham = get_object_or_404(SanPham, pk=c['MaSP'])
                cart.append({'SanPham': sanpham, 'SoLuong': c['SoLuong']})
            return render(request, 'giohang.html', {'Cart': cart})
    return render(request, 'giohang.html')

### API #########################################
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
def cap_nhat_so_luong(request):
    a = 1
    
@api_view(['POST'])
def them_gio_hang(request):
    msp = request.data.get('id')
    sanpham = get_object_or_404(SanPham, pk=msp)

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