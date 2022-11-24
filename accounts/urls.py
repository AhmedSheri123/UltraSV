from django.urls import path
from . import views

urlpatterns = [
    path('login', views.Login, name='login'),
    path('signup', views.Signup, name='signup'),
    path('logout', views.Logout, name='logout'),
    path('EmailValidation/<str:secret>', views.EmailValidation, name="EmailValidation"),
    path('SendSecretToValitedEmail/<str:lang>', views.SendSecretToValitedEmail, name="SendSecretToValitedEmail"),
    path('ForgetPassword', views.ForgetPassword, name='ForgetPassword'),
    path('PasswordReset/<str:secret>', views.PasswordReset, name="PasswordReset"),
]