from django.contrib import admin

# Register your models here.
from django.apps import apps

# Ensure you import the SanPham model
from .models import *

# Register the SanPham model with the PostAdmin class
class SanPhamAdmin(admin.ModelAdmin):
    list_filter = ['MaLoai__TenLoai']
    search_fields = ['MaSP', 'TenSP']

admin.site.register(SanPham, SanPhamAdmin)

class ChiTietKhoAdmin(admin.ModelAdmin):
    list_filter = ['MaKho']

admin.site.register(ChiTietKho, ChiTietKhoAdmin)

class HinhAnhSPAdmin(admin.ModelAdmin):
    search_fields = ['SanPham__MaSP']

admin.site.register(HinhAnhSP, HinhAnhSPAdmin)

class LoaiSPAdmin(admin.ModelAdmin):
    search_fields = ['MaLoai']

admin.site.register(Loai, LoaiSPAdmin)

# Register all other models in the 'TraiCay' app
app_models = apps.get_app_config('TraiCay').get_models()
for model in app_models:
    # Skip already registered models (like SanPham)
    if model not in admin.site._registry:
        admin.site.register(model)