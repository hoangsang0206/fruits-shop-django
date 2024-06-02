from rest_framework import serializers
from .models import Loai, SanPham, HinhAnhSP, ChiTietKho

class LoaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loai
        fields = '__all__'

class HinhAnhSpSerializer(serializers.ModelSerializer):
    class Meta:
        model = HinhAnhSP
        fields = '__all__'

class SanPhamSerializer(serializers.ModelSerializer):
    images = HinhAnhSpSerializer(many=True, read_only=True, source='hinhanhsp_set')
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = SanPham
        fields = '__all__'

    def get_quantity(self, obj):
        quantity = 0
        try:
            spkho = ChiTietKho.objects.filter(MaSP=sp)
            if spkho:
                for spk in spkho:
                    quantity += spk.SoLuongTon
        except:
            quantity = 0

        return quantity