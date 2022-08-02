from django.urls import path
from . import views

app_name = "excelapp"
urlpatterns = [
    path ("login", views.login, name="login"),
    path ("logout", views.logout, name="logout"),
    path ("generate-password", views.generate_password, name="generate-password"),
    path ("", views.home, name="home")
]