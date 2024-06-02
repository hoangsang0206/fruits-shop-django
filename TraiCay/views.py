from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import SanPham, HinhAnhSP, Loai, ChiTietKho, Slider

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import LoaiSerializer, SanPhamSerializer

# Create your views here.
def dangnhap(request):
    return render(request, 'dangnhap_dangky.html')

def home(request):
    Home_Fruits = []
    DSLoai = Loai.objects.all()[:7]
    for loai in DSLoai:
        fruits = []
        sanpham = SanPham.objects.filter(MaLoai = loai)
        for sp in sanpham:
            spkho = ChiTietKho.objects.filter(MaSP=sp)
            quantity = 0
            if spkho:
                for spk in spkho:
                    quantity += spk.SoLuongTon

            fruits.append({'fruit': sp, 'quantity': quantity, 'images': HinhAnhSP.objects.filter(SanPham = sp)})

        _Fruits = {'loai': loai, 'fruits': fruits}
        Home_Fruits.append(_Fruits)

    Sliders = Slider.objects.all()

    return render(request, 'home.html', {'Home_Fruits' : Home_Fruits, 'Sliders': Sliders})

def loc_theo_loai(request, id):
    if id == 'all':
        sanpham = SanPham.objects.all()
    else:
        loai = get_object_or_404(Loai, pk=id)
        sanpham = SanPham.objects.filter(MaLoai = loai)
    fruits = []
    for sp in sanpham:
        spkho = ChiTietKho.objects.filter(MaSP=sp)
        quantity = 0
        if spkho:
            for spk in spkho:
                quantity += spk.SoLuongTon

        fruits.append({'fruit': sp, 'quantity': quantity, 'images': HinhAnhSP.objects.filter(SanPham = sp)})

    return render(request, 'loai.html',{'Fruits': fruits} if id == 'all' else {'Loai': loai, 'Fruits': fruits})

def tim_kiem(request):
    query = request.GET.get('q')
    if query:
        sanpham = SanPham.objects.filter(TenSP__icontains=query)
    else:
        sanpham = SanPham.objects.all()
    fruits = []
    for sp in sanpham:
        spkho = ChiTietKho.objects.filter(MaSP=sp)
        quantity = 0
        if spkho:
            for spk in spkho:
                quantity += spk.SoLuongTon

        fruits.append({'fruit': sp, 'quantity': quantity, 'images': HinhAnhSP.objects.filter(SanPham = sp)})

    return render(request, 'timkiem.html', {'value': query, 'Fruits': fruits})

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


@api_view(['POST'])
def them_gio_hang(request):
    msp = request.POST.get('id')
    sanpham = get_object_or_404(SanPham, pk=msp)
