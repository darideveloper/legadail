import os
import json
from threading import Thread
from django.db import models
from django.dispatch import Signal
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .spreadsheet_manager.xlsx import SpreadSheetManager
from .views import notification_callback

def format_sheet_data (row): 
    if row[0] and type(row[0]) != str : 
        return [row[0].strftime("%H:%M"), *row[1:17]]
    else:
        return row[0:17]

def update_database (excel_file, ExcelFile):

    # Connect to notifier
    notifier = Signal()
    notifier.connect (receiver=notification_callback)

    # Submit start message
    notifier.send (sender="update_database", type="info", message="Loading new excel file. Wait before load more files.")
    
    # Connect to spreadsheet
    ssmanager = SpreadSheetManager(excel_file)

    # Get individuals from table
    ssmanager.set_sheet ("Individual")
    individuals_data = ssmanager.get_data ()
    individuals = list(map (lambda individual : individual[0], individuals_data))
    individuals = list(filter(lambda name : name != None, individuals))
    
    # Get individuals from sheets
    sheets = ssmanager.get_sheets ()

    # Filter individuals
    individuals = list(filter (lambda name : name in sheets, individuals))

    # Validate if the excel file its new
    excel_name = os.path.basename (excel_file)
    excel_files_users = ExcelFileUser.objects.filter (excel_file = ExcelFile)
    new_excel = False
    if len(excel_files_users) == 0:
        new_excel = True


    for individual in individuals:

        # Get shedule data from each individual sheet
        ssmanager.set_sheet (individual)
        sheet_data = ssmanager.get_data ()[1:80]
        
        # Clean shedule data
        sheet_data = list(map (format_sheet_data, sheet_data))
        sheet_data_json = {
            "data": sheet_data,
        }

        # Create new user
        if new_excel:

            # Create free name for the user
            username_counter = 0
            username = individual
            while True:
    
                # Format user name
                if username_counter > 0:
                    username = f"{individual} {username_counter}"

                # Get users in the database with the same name
                users_found = User.objects.filter (username = username)
                if users_found:
                    username_counter += 1
                    continue
                break

    
            # Create new users in database
            new_user = User (username=username)
            new_user.save ()

            # Save relationship between user and excel file
            new_excel_file_user = ExcelFileUser (user=new_user, excel_file=ExcelFile)
            new_excel_file_user.save()

            # Save individual schedule
            new_user_sheet_data = UserSheetData (user=new_user, data=sheet_data_json)
            new_user_sheet_data.save ()

        else:
        
            # Get current user
            possible_users = User.objects.filter (username__startswith=individual)
            excel_users = ExcelFileUser.objects.filter (user__in = possible_users)
            if len(excel_users) == 0:
                print ("no users found")
                continue
            current_user = excel_users[0].user

            # Save individual schedule
            current_user_sheet = UserSheetData.objects.filter (user=current_user)[0]
            current_user_sheet.data = sheet_data_json
            current_user_sheet.save ()

    notifier.send (sender="update_database", type="success", message="Done. Users added and schedule updated")

def validate_file_extension(value):
    """ Validate file extention in upload"""
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.xlsx', ".xlsm"]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Only ".xlsx" and "xlsm"')

class ExcelFile (models.Model):

    # Database
    name = models.CharField (max_length=100)
    comments = models.CharField (max_length=250, null=True, blank=True)
    file = models.FileField (upload_to="excelapp/static/excelapp/excel", validators=[validate_file_extension])

    class Meta:
        verbose_name_plural = "Excel files"
        verbose_name = "Excel file"

    # Extrac actions when save excel file
    def save (self):

        # Call to default save function
        super().save()

        # Create user when upload a new excel file
        # Call function in background
        thread_obj = Thread (target=update_database, args=(self.file.path, self))
        thread_obj.start ()
        # update_database (self.file.path, self)


class ExcelFileUser (models.Model):

    # database
    user = models.ForeignKey (User, on_delete=models.CASCADE, null=True)
    excel_file = models.ForeignKey (ExcelFile, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = "excel files users"
        verbose_name = "excel file user"

class UserSheetData (models.Model):
    # Database
    user = models.ForeignKey (User, on_delete=models.CASCADE, null=True)
    data = models.JSONField (null=True, blank=True)

    class Meta:
        verbose_name_plural = "users sheet data"
        verbose_name = "user sheet data"