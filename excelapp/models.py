import os
from threading import Thread
from django.db import models
from django.dispatch import Signal
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .spreadsheet_manager.xlsx import SpreadSheetManager
from .views import notification_callback

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
        sheet_data = map (lambda row : row[0:8], sheet_data)

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


        # Get individual schedule

        # Save individual schedule

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
    file = models.FileField (upload_to="excelapp/static/excelapp/excel", validators=[validate_file_extension])

    class Meta:
        verbose_name_plural = "excel files"
        verbose_name = "excel file"

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
    user = models.ForeignKey (User, on_delete=models.SET_NULL, null=True)
    excel_file = models.ForeignKey (ExcelFile, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "excel files users"
        verbose_name = "excel file user"