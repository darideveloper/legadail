from django.urls import path
from . import views

app_name = "excelapp"
urlpatterns = [
    path ("login", views.login, name="login"),
    path ("logout", views.logout, name="logout"),
    path ("generate-password", views.generate_password, name="generate-password"),
    path ("notification-get", views.notification_get, name="notification-get"),
    path ("notification-reset", views.notification_reset, name="notification-reset"),
    path ("", views.home, name="home")
]