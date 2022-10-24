from django.urls import path
from . import views
urlpatterns = [
    path('', views.Store, name="store"),
    path('ShowServices/<int:ServiesTypeId>', views.ShowServices, name="ShowServices"),
    path('ShowService/<int:ServiceId>', views.ShowService, name="ShowService"),
    path('getDownloadsLink/<int:ServiceId>', views.getDownloadsLink, name='getDownloadsLink')
]