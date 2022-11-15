from django.urls import path
from . import views

urlpatterns = [
    path('', views.tools, name="tools"),
    path('AllConvertImageFormatToAnother', views.AllConvertImageFormatToAnother, name="AllConvertImageFormatToAnother"),
    path('ConvertImageFormatToAnother/<str:id>', views.ConvertImageFormatToAnother, name="ConvertImageFormatToAnother"),
    path('imageConveringProcess', views.imageConveringProcess, name="imageConveringProcess"),
    path('html-to-pdf', views.HtmlToPdf, name="html-to-pdf"),
    path('taskDeleteConvertedImages', views.taskDeleteConvertedImages, name="taskDeleteConvertedImages"),
]