# Generated by Django 4.0.4 on 2022-08-03 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excelapp', '0005_alter_excelfile_file_excelfileuser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='excelfileuser',
            options={'verbose_name': 'excel file user', 'verbose_name_plural': 'excel files users'},
        ),
    ]
