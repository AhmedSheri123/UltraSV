from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('ChangeLanguage', views.ChangeLanguage, name='ChangeLanguage'),
    path('PrivacyPolicy', views.PrivacyPolicy, name="PrivacyPolicy"),
    path('TermsConditions', views.TermsConditions, name="TermsConditions")
]