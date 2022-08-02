import random
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

app_name = "Schedule App"

@login_required (login_url = "./login")
def home (request):

    context = {
        "app_name": app_name,
        "page_name": "Home",
        "pdf_path": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
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

