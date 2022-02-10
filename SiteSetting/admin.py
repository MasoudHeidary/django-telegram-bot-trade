from django.contrib import admin
from .models import SiteSetting


# Register your models here.

class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['PersianName', 'Name', 'Value']

    class Meta:
        object = SiteSetting


admin.site.register(SiteSetting, SiteSettingAdmin)
