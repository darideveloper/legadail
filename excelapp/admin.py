from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from . import models

class MyAdminSite(admin.AdminSite):
    site_header = 'Legadail Dashboar'
    site_title = 'Legadail Dashboar'
    
admin_site = MyAdminSite()

# Unregister defauls admin and groups
admin.site.unregister(User)
admin.site.unregister(Group)

# Setup agian admin and groups using django class
@admin.register(User)
class NewUserAdmin(UserAdmin):
    list_filter = ('is_staff','is_superuser')
    list_display = ('username','email','is_active', 'last_login')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@admin.register(models.ExcelFile)
class ExcelAdmin (admin.ModelAdmin):
    list_display = ('name',)
    ordering = ["name"]
    list_filter = ()

admin_site.register (User, NewUserAdmin)
admin_site.register (models.ExcelFile, ExcelAdmin)
