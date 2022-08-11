from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from . import models

class MyAdminSite(admin.AdminSite):
    site_header = 'Legadail Dashboar'
    site_title = 'Legadail'
    
admin_site = MyAdminSite()

# Unregister defauls admin and groups
admin.site.unregister(User)
admin.site.unregister(Group)

class ExcelUserListFilter (admin.SimpleListFilter):
    title = "Excel file"
    parameter_name = "get_excel"

    def lookups(self, request, model_admin):
        # Filter names in aside (value, name)

        excel_files = models.ExcelFile.objects.all ()
        return_data = map (lambda elem : (elem.name, elem.name), excel_files)

        return return_data

    def queryset (self, request, queryset):
        # Filter data

        if self.value():
            # Get valid users (ids)
            excel = models.ExcelFile.objects.filter (name=self.value())[0]
            excel_file_users = models.ExcelFileUser.objects.filter (excel_file = excel) 
            users_found_ids = list(map (lambda elem : elem.user.id, excel_file_users))

            # Filter user by ids
            return queryset.filter (id__in = users_found_ids)
        return queryset


# Setup agian admin and groups using django class
@admin.register(User)
class NewUserAdmin(UserAdmin):
    list_display = ('username','email','is_active', 'last_login', 'get_excel')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Fomrat excle custom field
    def get_excel (self, obj):
        excel_file_user = models.ExcelFileUser
        current_excel_file_user = excel_file_user.objects.filter (user = obj)
        if current_excel_file_user:
            excel_file = current_excel_file_user[0].excel_file.name
            return excel_file
        return ""

    get_excel.admin_order_field  = None  #Don't allows column order sorting
    get_excel.short_description = 'Excel File'  #Renames column head

    list_filter = ('is_staff', ExcelUserListFilter)

@admin.register(models.ExcelFile)
class ExcelAdmin (admin.ModelAdmin):
    list_display = ('name',)
    ordering = ["name"]
    list_filter = ()

admin_site.register (User, NewUserAdmin)
admin_site.register (models.ExcelFile, ExcelAdmin)
admin_site.register (models.ExcelFileUser)
admin_site.register (models.UserSheetData)
