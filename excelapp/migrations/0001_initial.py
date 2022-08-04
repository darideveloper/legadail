# Generated by Django 4.0.4 on 2022-08-04 08:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import excelapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('comments', models.CharField(max_length=250, null=True)),
                ('file', models.FileField(upload_to='excelapp/static/excelapp/excel', validators=[excelapp.models.validate_file_extension])),
            ],
            options={
                'verbose_name': 'Excel file',
                'verbose_name_plural': 'Excel files',
            },
        ),
        migrations.CreateModel(
            name='ExcelFileUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel_file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='excelapp.excelfile')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'excel file user',
                'verbose_name_plural': 'excel files users',
            },
        ),
    ]