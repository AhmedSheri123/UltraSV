from django.urls import path
from . import views
urlpatterns = [
    path('getNotification', views.SnippetList.as_view(), name='getNotification'),
    path('getImages', views.getViews.as_view(), name='getViews'),
]