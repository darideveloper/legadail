from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Legadail Admin'

urlpatterns = [
    path('', include("excelapp.urls")),
    path('admin', admin.site.urls)
]
