from django.contrib import admin

# Register your models here.
from django.apps import apps

app_models = apps.get_app_config('TraiCay').get_models()
for model in app_models:
    admin.site.register(model)