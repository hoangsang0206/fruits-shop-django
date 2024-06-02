from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import SanPham, HinhAnhSP, Loai, ChiTietKho, Slider

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import LoaiSerializer

# Create your views here.
@api_view(['GET'])
def getLoai(request):
    loai = Loai.objects.all()
    return Response(LoaiSerializer(loai, many=True).data)

def home(request):
    Home_Fruits = []
    DSLoai = Loai.objects.all()[:7]
    for loai in DSLoai:
        fruits = []
        sanpham = SanPham.objects.filter(MaLoai = loai)
        for sp in sanpham:
            try:
                quantity = ChiTietKho.objects.get(MaSP=sp)
                quantity = quantity.SoLuongTon
            except ChiTietKho.DoesNotExist:
                quantity = 0

            fruits.append({'fruit': sp, 'quantity': quantity, 'images': HinhAnhSP.objects.filter(SanPham = sp)})

        _Fruits = {'loai': loai, 'fruits': fruits}
        Home_Fruits.append(_Fruits)

    Sliders = Slider.objects.all()

    return render(request, 'home.html', {'Home_Fruits' : Home_Fruits, 'Sliders': Sliders})

def loc_theo_loai(request, id):
    loai = get_object_or_404(Loai, pk=id)
    sanpham = SanPham.objects.filter(MaLoai = loai)
    fruits = []
    for sp in sanpham:
            try:
                quantity = ChiTietKho.objects.get(MaSP=sp)
                quantity = quantity.SoLuongTon
            except ChiTietKho.DoesNotExist:
                quantity = 0

            fruits.append({'fruit': sp, 'quantity': quantity, 'images': HinhAnhSP.objects.filter(SanPham = sp)})

    return render(request, 'loai.html', {'Loai': loai, 'Fruits': fruits})

def tim_kiem(request):
    query = request.GET.get('q')
    if query:
        sanpham = SanPham.objects.filter(TenSP__icontains=query)
    else:
        sanpham = SanPham.objects.all()
    fruits = []
    for sp in sanpham:
            try:
                quantity = ChiTietKho.objects.get(MaSP=sp)
                quantity = quantity.SoLuongTon
            except ChiTietKho.DoesNotExist:
                quantity = 0

            fruits.append({'fruit': sp, 'quantity': quantity, 'images': HinhAnhSP.objects.filter(SanPham = sp)})

    return render(request, 'timkiem.html', {'value': query, 'Fruits': fruits})