from django.urls import path
from . import views

urlpatterns = [
    path('', views.Blog, name="blog"),
    path('ArticleType/<int:ArticleTypeId>', views.ShowArticles, name="ShowArticles"),
    path('Article/<int:ArticleId>', views.ShowArticle, name="ShowArticle"),
]