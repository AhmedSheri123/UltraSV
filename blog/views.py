from django.shortcuts import render
from .models import blogTypes, Article, ArticleTypes, ArticleViews
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
# Create your views here.


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def addVisitedItem(article, request):
    ip_address = get_client_ip(request)
    obj = ArticleViews.objects.filter(ip_address=ip_address, article=article, visited_date__date=timezone.now().date())
    if not obj.exists():
        obj = obj.create(ip_address=ip_address, article=article)
        obj.save()
        return True
    return False


def GetPagesData(article, page_number, number_of_list, last_pages_numbers_of_pages):
    next_pages = []
    prev_pages = []
    last_pages = []

    if page_number:
        page_number = int(page_number)

        number_of_list = int(number_of_list/2)
        page_range=article.paginator.page_range
        page_list = []
        
        for i in page_range:
            page_list.append(i)


        for i in range(page_number+1, page_number+number_of_list+1):
            if i<=0 or i > page_list[-1]:
                continue
            next_pages.append(str(i))
        for i in range(page_number-number_of_list, page_number):
            if i<=0:
                continue
            prev_pages.append(str(i))
        try:
            for i in range((last_pages_numbers_of_pages-1) - int(next_pages[-1]), page_list[-1]+1):
                if i<=int(next_pages[-1]):
                    continue
                last_pages.append(str(i))
        except:
            last_pages = []
    return next_pages, prev_pages, last_pages



def Blog(request):
    blog_types = blogTypes.objects.all()
    viewerCounter = ArticleViews.objects.all().count()
    return render(request, 'blog/blog.html', {'blog_types':blog_types, "viewerCounter":viewerCounter})

def ShowArticles(request, ArticleTypeId):
    blog_types = blogTypes.objects.get(id=ArticleTypeId)
    articles_types = ArticleTypes.objects.filter(blog=blog_types)
    article_url = request.build_absolute_uri()
    domain = get_current_site(request).domain
    article = Article.objects.filter(blogTypes=blog_types, is_enabled=True)
    filtering = request.GET.get('articletypes')
    searching = request.GET.get('search')

    if searching:
        article = article.filter(Q(title__icontains=searching))
        
    if filtering:
        if ',' in filtering:
            filtering = filtering.split(',')
        else:
            filtering = [filtering]
        article = article.filter(article_Type__id__in=filtering)
        article = list(dict.fromkeys(article))


    page_number = request.GET.get('page')
    number_of_list = 2
    last_pages_numbers_of_pages = 3
    paginator = Paginator(article, 2) # Show 25 contacts per page.
    article = paginator.get_page(page_number)
    next_pages, prev_pages, last_pages = GetPagesData(article, page_number, number_of_list, last_pages_numbers_of_pages)
    
    
    return render(request, 'blog/ShowArticles.html', {'blog_types': blog_types, 'article':article, 'articles_types':articles_types, "article_url":article_url, "domain":domain, "next_pages":next_pages, "prev_pages":prev_pages, "last_pages":last_pages, })

def ShowArticle(request, ArticleId):
    domain = get_current_site(request).domain
    article_url = request.build_absolute_uri()
    
    article = Article.objects.get(id=ArticleId, is_enabled=True)
    viewerCounter = ArticleViews.objects.all().count()
    addVisitedItem(article, request)
    return render(request, 'blog/ShowArticle.html', {'article':article, "article_url":article_url, "domain":domain, "viewerCounter":viewerCounter})