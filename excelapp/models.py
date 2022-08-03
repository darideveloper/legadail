import os
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

def validate_file_extension(value):
    """ Validate file extention in upload"""
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.xlsx']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Only ".xlsx"')

class ExcelFile (models.Model):

    # Database
    name = models.CharField (max_length=100)
    file = models.FileField (upload_to="excelapp/static/excelapp/excel", validators=[validate_file_extension])

    class Meta:
        verbose_name_plural = "excel files"
        verbose_name = "excel file"

class ExcelFileUser (models.Model):

    # database
    user = models.ForeignKey (User, on_delete=models.SET_NULL, null=True)
    excel_file = models.ForeignKey (ExcelFile, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "excel files users"
        verbose_name = "excel file user"