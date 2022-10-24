from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from blog.models import Article, blogTypes
# Create your views here.

def index(request):
    blog_types = blogTypes.objects.all()
    article_dict = []
    for blog_type in blog_types:
        article = Article.objects.filter(blogTypes=blog_type)[:3]
        article_dict.append(article)
    print(article_dict)
    return render(request, 'pages/index.html', {"article_dict":article_dict, "blog_types":blog_types})


def ChangeLanguage(request):
    if request.method == 'POST':
        lang = request.POST['language']
        next = request.POST['next']
        print(lang, next)
        return HttpResponseRedirect('/'+lang+next)
    else:
        return redirect('index')


def PrivacyPolicy(request):
    return render(request, 'pages/PrivacyPolicy.html')

def TermsConditions(request):
    return render(request, 'pages/TermsConditions.html')