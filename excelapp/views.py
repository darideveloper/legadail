import random
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as user_login, logout as user_logout, get_user
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

app_name = "Schedule App"
notification_data = {
    "type": None,
    "message": "",
}

@login_required (login_url = "./login")
def home (request):

    from .models import UserSheetData

    # Get sheet data from database
    user_name = get_user (request)
    current_user = User.objects.filter (username = user_name)[0]
    data_found = UserSheetData.objects.filter (user = current_user)
    if len(data_found) == 1:
        sheet_data = data_found[0].data
    else:
        sheet_data = {"data": [None, None]}
    
    context = {
        "app_name": app_name,
        "page_name": "Home",
        "pdf_path": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        "sheet_data_body": sheet_data["data"][1:],
        "sheet_data_header": sheet_data["data"][0]
    }
    return render (request, 'excelapp/home.html', context=context)

def login (request):
    """Login form in GET and validate login information and redirect to home in POST"""

    # Select random login for login form and context
    image_num = random.randint (1, 5)
    image_path = f"excelapp/imgs/illustration-{image_num}.svg"
    context = {
        "app_name": app_name,
        "page_name": "Login",
        "image_path": image_path,
        "message": ""
    }

    # GET
    if request.method == "GET":
        
        # Show login form
        return render (request, 'excelapp/login.html', context=context)

    # POST

    # Validate current user
    username = request.POST ["user"]
    password = request.POST ["password"]
    user = authenticate (username=username, password=password)
    if user:
        # Save user login
        user_login (request, user)

        # Redirect to home
        return redirect ("./")
    else:
        # redirect to login form with error message if credentials are wrong
        context["message"] = "Wrong user or password. Try again."
        return render (request, 'excelapp/login.html', context=context)

def logout (request):

    # End user session
    user_logout (request)

    # Redirect to login
    return redirect ("./login")

def generate_password (request):

    # Select random login for login form and create context
    image_num = random.randint (1, 5)
    image_path = f"excelapp/imgs/illustration-{image_num}.svg"
    context = {
        "app_name": app_name,
        "page_name": "Generate Password",
        "image_path": image_path,
        "message": ""
    }

    # GET
    if request.method == "GET":
        
        # Show login form
        return render (request, 'excelapp/generate_password.html', context=context)

    # POST

    # Get user and new password
    username = request.POST ["user"]
    password = request.POST ["password1"]

    # Valide if user dont have password yet
    user = User.objects.get(username=username)
    if user.password:
        # Create error message
        context["message"] = "The user already have a password. If you have problems contact the admin."
    else: 
        # Save new password
        user.set_password (password)
        user.save ()

        # Create confirmation message
        context["message"] = "Password created. Now you can login in main page"
    
    # Show page with message
    return render (request, 'excelapp/generate_password.html', context=context)

def notification_get (request):
    return JsonResponse (notification_data)

def notification_reset (request):
    notification_data["type"] = None
    notification_data["message"] = ""
    return HttpResponse ("done")

def notification_callback (sender, **kwargs):
    # Update notification data
    notification_data["type"] = kwargs["type"]
    notification_data["message"] = kwargs["message"]