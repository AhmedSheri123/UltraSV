from django.shortcuts import render
from .models import Services, ServiceTypes, StoreTypes, ServiceViews, ServicesDownloads, download_size_type_list
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q 
from dashboard.countrys import get_location
from dashboard.models import VisitPriceByCountry
# Create your views here.

def addServiceDownloadCounter(request, service):
    ip_address = get_client_ip(request)
    obj = ServicesDownloads.objects.filter(ip_address=ip_address, service=service, downloaded_date__date=timezone.now().date())
    if not obj.exists():
        obj = obj.create(ip_address=ip_address, service=service)
        obj.save()
        return True
    return False

def getMonyByCountry(country_code):
        visit_price_by_country = VisitPriceByCountry.objects.filter(country=country_code)
        
        if visit_price_by_country.exists():
            return visit_price_by_country.filter(country=country_code)[0].price_per_one_visit
        else:
            return VisitPriceByCountry.objects.get(country='others').price_per_one_visit



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def addVisitedItem(service, request):
    ip_address = '122.169.13.83'# get_client_ip(request)

    obj = ServiceViews.objects.filter(ip_address=ip_address, visited_date__date=timezone.now().date())
    
    if not obj.exists():
        data = get_location(ip_address)
        country_code=data.get('country_code')
        
        obj = obj.create(ip_address=ip_address, service=service, country_code=country_code, country_name=data.get('country_name'), city=data.get('city'), region=data.get('region'), earn_count=getMonyByCountry(country_code))
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


def Store(request):
    viewerCounter = ServiceViews.objects.all().count()
    store_types = StoreTypes.objects.all()
    return render(request, 'store/store.html', {'store_types':store_types, "viewerCounter":viewerCounter})

def ShowServices(request, ServiesTypeId):
    store_types = StoreTypes.objects.get(id=ServiesTypeId)
    services_types = ServiceTypes.objects.filter(store=store_types)
    service_url = request.build_absolute_uri()
    domain = get_current_site(request).domain
    service = Services.objects.filter(storeTypes=store_types, is_enabled=True)
    filtering = request.GET.get('ServiesTypes')
    searching = request.GET.get('search')

    if searching:

        service = service.filter(Q(title__icontains=searching))
    if filtering:
        if ',' in filtering:
            filtering = filtering.split(',')
        else:
            filtering = [filtering]
        service = service.filter(service_Type__id__in=filtering)
        service = list(dict.fromkeys(service))

    page_number = request.GET.get('page')
    number_of_list = 2
    last_pages_numbers_of_pages = 3
    paginator = Paginator(service, 2) # Show 25 contacts per page.
    service = paginator.get_page(page_number)
    next_pages, prev_pages, last_pages = GetPagesData(service, page_number, number_of_list, last_pages_numbers_of_pages)


    return render(request, 'store/Services.html', {'store_types': store_types, 'service':service, 'services_types':services_types, "service_url":service_url, "domain":domain, "next_pages":next_pages, "prev_pages":prev_pages, "last_pages":last_pages,})

def ShowService(request, ServiceId):
    domain = get_current_site(request).domain
    service_url = request.build_absolute_uri()
    service = None
    if Services.objects.filter(id=ServiceId, user=request.user, is_visible_to_the_user=True).exists() or request.user.is_superuser:
        service = Services.objects.get(id=ServiceId)
    else:
        service = Services.objects.get(id=ServiceId, is_enabled=True)

    serviceDownloaded = ServicesDownloads.objects.filter(service=service).count()


    file_size_format = None
    for i in download_size_type_list:
        if i[0] == service.file_size_format:
            file_size_format = i[1]
            break


    #addVisitedItem(service, request)
    viewerCounter = ServiceViews.objects.filter(service=service).count()
    return render(request, 'store/Service.html', {'service':service, "service_url":service_url, "domain":domain, "serviceDownloaded":serviceDownloaded, "viewerCounter":viewerCounter, 'file_size_format':file_size_format})



def getDownloadsLink(request, ServiceId):
    url = ''
    service = get_object_or_404(Services, id=ServiceId, show_download_button=True, is_enabled=True)
    if service.is_from_url:
        url = service.service_url
    elif service.is_from_local:
        url = service.service_file.url
    addServiceDownloadCounter(request, service)
    #return HttpResponseRedirect(url)
    return render(request, 'getDownloadsLink.html', {'url':url, 'ServiceId':ServiceId})