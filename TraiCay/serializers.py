from rest_framework import serializers
from .models import Loai

class LoaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loai
        fields = '__all__'