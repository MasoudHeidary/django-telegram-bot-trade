from django.contrib import admin

from .models import Luck, LuckSetting


# Register your models here.

class LuckAdmin(admin.ModelAdmin):
    list_display = ['id', 'UserID', 'Name', 'Paied']
    search_fields = ['UserID']
    list_filter = ['Paied']
    list_editable = ['Paied']

    class Meta:
        object = Luck


class LuckSettingAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name', 'Number']

    class Meta:
        object = LuckSetting


admin.site.register(Luck, LuckAdmin)
admin.site.register(LuckSetting, LuckSettingAdmin)
