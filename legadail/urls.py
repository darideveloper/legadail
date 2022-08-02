from excelapp.admin import admin_site
from django.urls import path, include

urlpatterns = [
    path('', include("excelapp.urls")),
    path('admin', admin_site.urls)
]
