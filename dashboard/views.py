from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from store.models import Services, ServiceTypes, StoreTypes, ServiceViews, ServicesDownloads, WaitForAccept, download_size_type_list, EditedServicesWaitForAccept
from blog.models import blogTypes, Article, ArticleTypes, ArticleViews, WaitArticlesForAccept, EditedArticlesWaitForAccept
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q 
from store.views import GetPagesData
from .forms import AddNewServiceForMeForm, UserProfileForm, UserForm
from django.utils import timezone
from django.contrib import messages
from accounts.models import Notification, VerifiedEmail
import translators as tss
import datetime
from django.http import HttpResponseRedirect
from .models import VisitPriceByCountry
from accounts.models import Withdraw, withdrawal_method_list
from calendar import monthrange
from accounts.SendEmail import send_email
from django.utils.translation import get_language

# Create your views here.

def WithdrawDelete(request, id):
    if request.user.is_superuser:
        REFERER = request.META['HTTP_REFERER']
        withdraws = Withdraw.objects.get(id=id)
        withdraws.delete()

        return redirect(REFERER)

def WithdrawComplete(request, id):
    if request.user.is_superuser:
        REFERER = request.META['HTTP_REFERER']
        withdraws = Withdraw.objects.get(id=id)
        withdraws.status = '2'
        withdraws.save()

        notif = Notification.objects.create(sender=request.user, receiver=withdraws.user)
        link = '/dashboard/Withdrawn'
        notif.message_en = f'The draw has been completed successfully {withdraws.total_amount} to view <a style="color: #438fff;" href={link} target="_blank">Click here</a>'
        notif.message_ar = f'تم الانتهاء من عملية السحب بنجاح بقيمة {withdraws.total_amount} للمشاهدة <a style="color: #438fff;" href={link} target="_blank">اضغط هنا</a>'
        userprofile = withdraws.user.userprofile
        userprofile.is_not_read_notification = True
        userprofile.money = userprofile.money - withdraws.total_amount
        userprofile.save()
        notif.save()        
        return redirect(REFERER)

def WithdrawCancel(request, id):
    if request.user.is_superuser:
        
        if request.method == 'POST':

            REFERER = request.META['HTTP_REFERER']
            withdraws = Withdraw.objects.get(id=id)
            userprofile = withdraws.user.userprofile
            if withdraws.status == '2':
                userprofile.money += withdraws.total_amount
                
            withdraws.status = '3'
            withdraws.save()
            msg = request.POST.get('msg')
            
            notif = Notification.objects.create(sender=request.user, receiver=withdraws.user)
            notif.message_en = tss.google(msg, to_language='en')
            notif.message_ar = tss.google(msg, to_language='ar')
            userprofile.is_not_read_notification = True
            userprofile.save()
            notif.save() 
    
            return redirect(REFERER)

def WithdrawAccept(request, id):
    if request.user.is_superuser:
        REFERER = request.META['HTTP_REFERER']
        withdraws = Withdraw.objects.get(id=id)
        withdraws.status = '1'
        withdraws.save()
        return redirect(REFERER)

def dashboardWithdraw(request):
    data = request.GET
    filter_enabled = data.get('filter_enabled')
    withdraws = Withdraw.objects.filter()
    filter_list = []
    if data.get('Pending'):
        filter_list.append('0')

    if data.get('Accepted'):
        filter_list.append('1')

    if data.get('Completed'):
        
        filter_list.append('2')

    if data.get('Canceled'):
        filter_list.append('3')
    if filter_enabled:
        withdraws = withdraws.filter(status__in=filter_list)
    Pending = withdraws.filter(status='0').count()
    accepted = withdraws.filter(status='1').count()
    Completed = withdraws.filter(status='2').count()
    Canceled = withdraws.filter(status='3').count()

    return render(request, 'dashboard/admin/dashboardWithdraw.html', {'withdraws':withdraws, 'accepted':accepted,
    'Completed':Completed, 'Canceled':Canceled, 'Pending':Pending, 'Pending_form': data.get('Pending'), 
    'Accepted_form': data.get('Accepted'), 'Completed_form' : data.get('Completed'), 'Canceled_form': data.get('Canceled'), 'filter_enabled': filter_enabled})

def Withdrawn(request):
    user = request.user
    withdraw = Withdraw.objects.filter(user=user)
    Pending = withdraw.filter(status__in=['0','1'])
    Completed = withdraw.filter(status='2')
    TotalAmountPendingMoney = 0
    TotalAmountWithdrawnMoney = 0

    for i in Completed:
        TotalAmountWithdrawnMoney += i.total_amount
    for i in Pending:
        TotalAmountPendingMoney += i.total_amount
        
    money_now = request.user.userprofile.money-TotalAmountPendingMoney
    if request.method == 'POST':
        data = request.POST
        withdrawn_type = data.get('withdrawn_type')
        amount = data.get('amount')
        desc = data.get('desc')

        if float(money_now) >= float(amount):
            if float(amount) >= 3:
                obj = withdraw.create(user=user, status='0', withdrawal_method=withdrawn_type, total_amount=amount, desc=desc)
                obj.save()
                return redirect('Withdrawn')
            else:
                messages.error(request, 'يجب ان تسحب على الاقل 3 دولار')
                
        else:
            messages.error(request, 'ليس لديك رصيد كافي')
    return render(request, 'dashboard/withdraw.html', {'withdrawal_method':withdrawal_method_list, 'withdraws':withdraw, 'TotalAmountPendingMoney':TotalAmountPendingMoney, 'TotalAmountWithdrawnMoney':TotalAmountWithdrawnMoney, 'money_now':money_now})


def getDomain(request):
    domain = get_current_site(request).domain
    return domain


def main(request):
    base = timezone.now()
    visit_price_by_country = VisitPriceByCountry.objects.all()
    for i in visit_price_by_country:
        i.price_per_one_visit *=1000

    date_list = [base.date().replace(day=1) + datetime.timedelta(days=x) for x in range(monthrange(base.year, base.month)[1])]
    articles = ArticleViews.objects.filter()
    services = ServiceViews.objects.filter()

    articles_view_count = articles.filter(article__user=request.user).count()
    services_view_count = services.filter(service__user=request.user).count()
    
    def getMonyByCountry(views_model):
        get_money_by_country = 0
        for i in views_model:
            get_money_by_country += i.earn_count
        return get_money_by_country

    services_money_by_month = getMonyByCountry(services.filter(visited_date__year=base.year, visited_date__month=base.month, service__user=request.user))
    articles_money_by_month = getMonyByCountry(articles.filter(visited_date__year=base.year, visited_date__month=base.month, article__user=request.user))

    articles_views_per_month = articles.filter(visited_date__year=base.year, visited_date__month=base.month, article__user=request.user).count()
    services_views_per_month = services.filter(visited_date__year=base.year, visited_date__month=base.month, service__user=request.user).count()
    articles_views_per_day = []
    services_views_per_day = []
    for i in date_list:
        articles_views_per_day.append(articles.filter(visited_date__date=i, article__user=request.user).count())
        services_views_per_day.append(services.filter(visited_date__date=i, service__user=request.user).count())


    #views by months
    month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    articles_money_by_12month = []
    services_money_by_12month = []
    for i in month:
        month_money = 0 
        month_money2 = 0
        a = articles.filter(visited_date__year=base.year, visited_date__month=i, article__user=request.user)
        b = services.filter(visited_date__year=base.year, visited_date__month=i, service__user=request.user)
        for article in a:
            month_money += article.earn_count
        for service in b:
            month_money2 += service.earn_count

        articles_money_by_12month.append(str(float(month_money)))
        services_money_by_12month.append(str(float(month_money2)))
    
    
    return render(request, 'dashboard/main.html', {'articles_views_per_day':reversed(articles_views_per_day), 
    'date_list':reversed(date_list), 'services_views_per_day':reversed(services_views_per_day), 
    'articles_views_per_month':articles_views_per_month, 'services_views_per_month':services_views_per_month, 
    'articles_view_count':articles_view_count, 'services_view_count':services_view_count, 
    'services_money_by_month':str(services_money_by_month), 'articles_money_by_month':str(articles_money_by_month) 
    ,'articles_money_by_12month':articles_money_by_12month, 'services_money_by_12month':services_money_by_12month, 
    'user_money':str(request.user.userprofile.money), 'visit_price_by_country':visit_price_by_country})
    
def mySotre(request):
    viewerCounter = ServiceViews.objects.all().count()
    store_types = StoreTypes.objects.all()
    return render(request, 'dashboard/store/store.html', {'store_types':store_types, "viewerCounter":viewerCounter})


def myServices(request, ServiesTypeId):

    store_types = StoreTypes.objects.get(id=ServiesTypeId)
    services_types = ServiceTypes.objects.filter(store=store_types)
    service_url = request.build_absolute_uri()
    domain = get_current_site(request).domain
    service = Services.objects.filter(storeTypes=store_types, user=request.user)

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
    paginator = Paginator(service, 10) # Show 25 contacts per page.
    service = paginator.get_page(page_number)
    next_pages, prev_pages, last_pages = GetPagesData(service, page_number, number_of_list, last_pages_numbers_of_pages)


    return render(request, 'dashboard/store/Services.html', {'store_types': store_types, 'service':service, 'services_types':services_types, "service_url":service_url, "domain":domain, "next_pages":next_pages, "prev_pages":prev_pages, "last_pages":last_pages})

def AddNewServiceForMe(request, store_id):
    # service download list sizes
    language = get_language()

    form = AddNewServiceForMeForm
    service_types = ServiceTypes.objects.filter(store__id = store_id)
    if request.method == 'POST':
        #get requested fields

        title_ar = request.POST.get('title_ar')
        desc_ar = request.POST.get('desc_ar')
        content_ar = request.POST.get('content_ar')
        keyword_ar = request.POST.get('keyword_ar')
        title_en = request.POST.get('title_en')
        desc_en = request.POST.get('desc_en')
        content_en = request.POST.get('content_en')
        keyword_en = request.POST.get('keyword_en')
        service_type = request.POST.getlist('service_type')
        image = request.FILES.get('image')
        download_url = request.POST.get('download_url')
        service_version = request.POST.get('service_version')
        download_size_type = request.POST.get('download_size_type')
        download_size = request.POST.get('download_size')
        issued = request.POST.get('issued')
        SaveAsDraft = request.POST.get('SaveAsDraft')
        
        service = Services.objects.create(user=request.user, title_ar=title_ar, title_en=title_en, desc_ar=desc_ar, desc_en=desc_en, keyword_ar=keyword_ar, keyword_en=keyword_en, article_ar=content_ar, article_en=content_en, service_version=service_version)
        #set store type
        service.storeTypes = StoreTypes.objects.get(id=store_id)

        # set service type many to many
        service.service_Type.set(ServiceTypes.objects.filter(id__in=service_type))

        #set image
        service.article_img = image

        #set download url
        service.is_from_url = True
        service.service_url = download_url
        
        # set service file size
        service.file_size = download_size
        service.file_size_format = download_size_type
        
        #set issued date
        if issued:
            issued = datetime.datetime.strptime(issued, '%Y-%m-%d')
        else:
            issued = None
        service.issued = issued

        # set service published to False
        service.is_enabled = False

        #set image desc 
        service.img_desc_ar = title_ar
        service.img_desc_en = title_en

        # set SaveAsDraft
        if SaveAsDraft == '1':
            service.save_as_draft = True

        service.save()

        if not SaveAsDraft == '1':
            wait_for_accept = WaitForAccept.objects.create(service=service, publish_date=timezone.now())
            wait_for_accept.save()
            if language == 'ar':
                messages.success(request, 'طلبك قيد المراجعة سوف يتم نشر خدمتك بعد المراجعة')
            else:
                messages.success(request, 'Your application is under review Your service will be posted after review')
        else:
            if language == 'ar':
                messages.success(request, 'تم حفظ الخدمة كمسودة')
            else:
                messages.success(request, 'The service has been saved as a draft')

        return redirect('myServices', service.storeTypes.id)
    return render(request, 'dashboard/store/AddNewServiceForMe.html', {'form':form, 'service_type':service_types, 'download_size_type_list':download_size_type_list})

def DeleteMyService(request, id):
    service = Services.objects.filter(id=id, user=request.user)[0]
    service.delete()
    return redirect('myServices', service.storeTypes.id)



def EditServiceForMe(request, service_id):
    language = get_language()
    form = AddNewServiceForMeForm
    service = None
    edited_service_is_exists =None
    if request.user.is_superuser:
        service = Services.objects.get(id=service_id)
        edited_service = EditedServicesWaitForAccept.objects.filter(service=service)
    else:
        service = Services.objects.get(id=service_id, user=request.user)
        edited_service = EditedServicesWaitForAccept.objects.filter(user=request.user, service=service)

    edited_service_is_exists = edited_service.exists()

    service_model = service
    if edited_service_is_exists:
        service = edited_service[0]
        service_model = service.service

    # get service data from database
    title_ar = service.title_ar
    desc_ar = service.desc_ar
    content_ar = service.article_ar
    keyword_ar = service.keyword_ar
    title_en = service.title_en
    desc_en = service.desc_en
    content_en = service.article_en
    keyword_en = service.keyword_en
    service_type = service.service_Type
    image = service.article_img
    download_url = service.service_url
    service_version = service.service_version
    download_size = service.file_size
    file_size_format = service.file_size_format
    issued = service.issued
    SaveAsDraft = service.save_as_draft

    service_types = ServiceTypes.objects.filter(store = service_model.storeTypes)

    obj = {
        'title_ar': title_ar,
        'desc_ar': desc_ar,
        'content_ar': content_ar,
        'keyword_ar': keyword_ar,
        'title_en': title_en,
        'desc_en': desc_en,
        'content_en': content_en,
        'keyword_en': keyword_en,
        'service_type': service_type.all(),
        'image': image,
        'download_url': download_url,
        'service_version': service_version,
        'download_size': download_size,
        'file_size_format' : file_size_format,
        'issued': str(issued),
        'SaveAsDraft': SaveAsDraft,
        'service_types': service_types,
        'form':form,
        'download_size_type_list':download_size_type_list
    }

    #set SaveAsDraft to num
    if obj['SaveAsDraft'] == True:
        obj['SaveAsDraft'] = '1'
    else:
        obj['SaveAsDraft'] = '0'

    if request.method == 'POST':
        #get requested data
        title_ar = request.POST.get('title_ar')
        desc_ar = request.POST.get('desc_ar')
        content_ar = request.POST.get('content_ar')
        keyword_ar = request.POST.get('keyword_ar')
        title_en = request.POST.get('title_en')
        desc_en = request.POST.get('desc_en')
        content_en = request.POST.get('content_en')
        keyword_en = request.POST.get('keyword_en')
        service_type = request.POST.getlist('service_type')
        image = request.FILES.get('image')
        download_url = request.POST.get('download_url')
        service_version = request.POST.get('service_version')
        download_size_type = request.POST.get('download_size_type')
        download_size = request.POST.get('download_size')
        issued = request.POST.get('issued')
        SaveAsDraft = request.POST.get('SaveAsDraft')

        

        #delete all avarible edited service for create new one
        if edited_service.exists():
            for i in edited_service:
                i.delete()

        # set SaveAsDraft
        if SaveAsDraft == '1':
            service = Services.objects.get(id=service_model.id)

            service.save_as_draft = True
            service.is_enabled = False
            
            service.title_ar = title_ar
            service.desc_ar = desc_ar
            service.article_ar = content_ar
            service.keyword_ar = keyword_ar
            service.title_en = title_en
            service.desc_en = desc_en
            service.article_en = content_en
            service.keyword_en = keyword_en
            service.service_Type.set(ServiceTypes.objects.filter(id__in=service_type))
            service.service_url = download_url
            service.service_version = service_version
            service.file_size_format = download_size_type
            service.file_size = download_size

            #set issued date
            if issued:
                issued = datetime.datetime.strptime(issued, '%Y-%m-%d')
            else:
                issued = None
            service.issued = issued

            #set image desc 
            service.img_desc_ar = title_ar
            service.img_desc_en = title_en

            #set image if exists
            if image:
                service.article_img = image

            if language == 'ar':
                messages.success(request, 'تم حفظ الخدمة كمسودة')
            else:
                messages.success(request, 'The service has been saved as a draft')
            service.save()
        else:

            if language == 'ar':
                messages.success(request, 'طلبك قيد المراجعة سوف يتم نشر خدمتك بعد المراجعة')
            else:
                messages.success(request, 'Your application is under review Your service will be posted after review')

                
            edited_service_create = EditedServicesWaitForAccept.objects.create(user=request.user, service=service_model)

            
            edited_service_create.title_ar = title_ar
            edited_service_create.desc_ar = desc_ar
            edited_service_create.article_ar = content_ar
            edited_service_create.keyword_ar = keyword_ar
            edited_service_create.title_en = title_en
            edited_service_create.desc_en = desc_en
            edited_service_create.article_en = content_en
            edited_service_create.keyword_en = keyword_en
            edited_service_create.service_Type.set(ServiceTypes.objects.filter(id__in=service_type))
            edited_service_create.service_url = download_url
            edited_service_create.service_version = service_version
            edited_service_create.file_size_format = download_size_type
            edited_service_create.file_size = download_size
            



            #set issued date
            if issued:
                issued = datetime.datetime.strptime(issued, '%Y-%m-%d')
            else:
                issued = None
            edited_service_create.issued = issued

            #set image desc 
            edited_service_create.img_desc_ar = title_ar
            edited_service_create.img_desc_en = title_en

            #set image if exists
            if image:
                edited_service_create.article_img = image
                

            edited_service_create.save()


        return redirect('myServices', service_model.storeTypes.id)

    return render(request, 'dashboard/store/EditServiceForMe.html', obj)


def RequestsUnderReview(request):
    return render(request, 'dashboard/admin/requests__under_review.html')



def requestsUnderReviewServices(request):
    wait_for_accept = WaitForAccept.objects.all()

    return render(request, 'dashboard/admin/requests_under_review_services.html', {'wait_for_accept':wait_for_accept})



def requestsUnderReviewServicesAccept(request, WaitForAcceptID):
    

    wait_for_accept = WaitForAccept.objects.get(id=WaitForAcceptID)
    service = wait_for_accept.service
    service.is_enabled = True
    service.save()
    wait_for_accept.delete()
    
    #get service link
    
    service_link = f'/store/ShowService/{service.id}'
    #send Notification
    notif_msg_ar = f"""
    <p dir='rtl'>تهانينا تم قبول خدمتك "{service.title}" لمشاهدتها <a style="color: #438fff;" href='{service_link}' target='_blank'>اضغط هنا</a></p>
    """
    notif_msg_en = f"""
    <p dir='rtl'>Congratulations, your service "{service.title}" has been accepted, to view it <a style="color: #438fff;" href='{service_link}' target='_blank'>click here</a></p>
    """
    notif = Notification.objects.create(sender=request.user,receiver=service.user)
    notif.message_en = notif_msg_en
    notif.message_ar = notif_msg_ar
    userprofile = service.user.userprofile
    userprofile.is_not_read_notification = True
    userprofile.save()
    notif.save()

    return redirect('requestsUnderReviewServices')


def requestsUnderReviewSrvicesCancel(request, WaitForAcceptID):
    if request.method == 'POST':
        msg = request.POST.get('msg')
        wait_for_accept = WaitForAccept.objects.get(id=WaitForAcceptID)
        service = wait_for_accept.service
        service.is_enabled = False
        service.save_as_draft = True
        service.save()
        wait_for_accept.delete()

        msg = str(msg).format(username=service.user.username, title=service.title, id=service.id)
        notif = Notification.objects.create(sender=request.user,receiver=service.user)
        notif.message_en = tss.google(msg, to_language='en')
        notif.message_ar = tss.google(msg, to_language='ar')
        userprofile = service.user.userprofile
        userprofile.is_not_read_notification = True
        userprofile.save()
        notif.save()
        return redirect('requestsUnderReviewServices')



def requestsUnderReviewEditedServices(request):
    wait_for_accept = EditedServicesWaitForAccept.objects.filter(modification_cancelled=False)

    return render(request, 'dashboard/admin/requests_under_review_edited_services.html', {'wait_for_accept':wait_for_accept})



def requestsUnderReviewEditedServicesAccept(request, WaitForAcceptID):
    wait_for_accept = EditedServicesWaitForAccept.objects.get(id=WaitForAcceptID)
    service = wait_for_accept.service

    # get edited data from database
    title_ar = wait_for_accept.title_ar
    desc_ar = wait_for_accept.desc_ar
    content_ar = wait_for_accept.article_ar
    keyword_ar = wait_for_accept.keyword_ar
    title_en = wait_for_accept.title_en
    desc_en = wait_for_accept.desc_en
    content_en = wait_for_accept.article_en
    keyword_en = wait_for_accept.keyword_en
    service_type = wait_for_accept.service_Type
    image = wait_for_accept.article_img
    download_url = wait_for_accept.service_url
    service_version = wait_for_accept.service_version
    download_size = wait_for_accept.file_size
    file_size_format = wait_for_accept.file_size_format
    issued = wait_for_accept.issued


    # set service data to edited data
    service.title_ar = title_ar
    service.desc_ar = desc_ar
    service.article_ar = content_ar
    service.keyword_ar = keyword_ar
    service.title_en = title_en
    service.desc_en = desc_en
    service.article_en = content_en
    service.keyword_en = keyword_en
    service.service_Type.set(service_type.all())
    if image:
        service.article_img = image
    service.service_url = download_url
    service.service_version = service_version
    service.file_size = download_size
    service.file_size_format = file_size_format
    service.issued = issued

    service.save()

    service.is_enabled = True
    service.save_as_draft = False
    service.save()
    wait_for_accept.delete()



    #get service link
    
    service_link = f'/store/ShowService/{service.id}'
    #send Notification
    notif_msg_ar = f"""
        <p dir = 'rtl'> تهانينا ، تم الموافقة على التعديل الذي أجريته على خدمتك "{service.title}" لعرض <a style="color: #438fff;" href='{service_link}' target='_ blank'> انقر هنا </a> </p>
    """
    notif_msg_en = f"""
        <p dir='rtl'>Congratulations, your edit to your service "{service.title}" has been accepted for viewing <a style="color: #438fff; text-decoration: underline;" href='{service_link}' target='_blank'>Click here</a></p>
    """
    notif = Notification.objects.create(sender=request.user,receiver=service.user)
    notif.message_en = notif_msg_en
    notif.message_ar = notif_msg_ar
    userprofile = service.user.userprofile
    userprofile.is_not_read_notification = True
    userprofile.save()
    notif.save()


    return redirect('requestsUnderReviewEditedServices')


def requestsUnderReviewEditedSrvicesCancel(request, WaitForAcceptID):
    if request.method == 'POST':
        msg = request.POST.get('msg')
        wait_for_accept = EditedServicesWaitForAccept.objects.get(id=WaitForAcceptID)
        wait_for_accept.modification_cancelled = True
        wait_for_accept.save()


        msg = str(msg).format(username=wait_for_accept.user.username, title=wait_for_accept.title, id=wait_for_accept.id)
        notif = Notification.objects.create(sender=request.user,receiver=wait_for_accept.user)
        notif.message_en = tss.google(msg, to_language='en')
        notif.message_ar = tss.google(msg, to_language='ar')
        userprofile = wait_for_accept.user.userprofile
        userprofile.is_not_read_notification = True
        userprofile.save()
        notif.save()
    return redirect('requestsUnderReviewEditedServices')


def myBlog(request):
    viewerCounter = ArticleViews.objects.all().count()
    store_types = blogTypes.objects.all()
    return render(request, 'dashboard/blog/myBlog.html', {'blog_types':store_types, "viewerCounter":viewerCounter})



def myArticles(request, ServiesTypeId):

    store_types = StoreTypes.objects.get(id=ServiesTypeId)
    services_types = ServiceTypes.objects.filter(store=store_types)
    service_url = request.build_absolute_uri()
    domain = get_current_site(request).domain
    service = Services.objects.filter(storeTypes=store_types, user=request.user)

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
    paginator = Paginator(service, 10) # Show 25 contacts per page.
    service = paginator.get_page(page_number)
    next_pages, prev_pages, last_pages = GetPagesData(service, page_number, number_of_list, last_pages_numbers_of_pages)


    return render(request, 'dashboard/store/Services.html', {'store_types': store_types, 'service':service, 'services_types':services_types, "service_url":service_url, "domain":domain, "next_pages":next_pages, "prev_pages":prev_pages, "last_pages":last_pages})


def myArticles(request, ArticleTypeId):
    blog_types = blogTypes.objects.get(id=ArticleTypeId)
    articles_types = ArticleTypes.objects.filter(blog=blog_types)
    article_url = request.build_absolute_uri()
    domain = get_current_site(request).domain
    article = Article.objects.filter(blogTypes=blog_types, user=request.user)
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
    
    
    return render(request, 'dashboard/blog/myArticles.html', {'blog_types': blog_types, 'article':article, 'articles_types':articles_types, "article_url":article_url, "domain":domain, "next_pages":next_pages, "prev_pages":prev_pages, "last_pages":last_pages, })








def AddNewArticleForMe(request, blog_id):
    # service download list sizes
    language = get_language()

    form = AddNewServiceForMeForm
    service_types = ArticleTypes.objects.filter(blog__id = blog_id)
    if request.method == 'POST':
        #get requested fields

        title_ar = request.POST.get('title_ar')
        desc_ar = request.POST.get('desc_ar')
        content_ar = request.POST.get('content_ar')
        keyword_ar = request.POST.get('keyword_ar')
        title_en = request.POST.get('title_en')
        desc_en = request.POST.get('desc_en')
        content_en = request.POST.get('content_en')
        keyword_en = request.POST.get('keyword_en')
        service_type = request.POST.getlist('service_type')
        image = request.FILES.get('image')
        
        SaveAsDraft = request.POST.get('SaveAsDraft')
        
        service = Article.objects.create(user=request.user, title_ar=title_ar, title_en=title_en, desc_ar=desc_ar, desc_en=desc_en, keyword_ar=keyword_ar, keyword_en=keyword_en, article_ar=content_ar, article_en=content_en)
        #set store type
        service.blogTypes = blogTypes.objects.get(id=blog_id)

        # set service type many to many
        service.article_Type.set(ArticleTypes.objects.filter(id__in=service_type))

        #set image
        service.article_img = image

        # set service published to False
        service.is_enabled = False

        #set image desc 
        service.img_desc_ar = title_ar
        service.img_desc_en = title_en

        # set SaveAsDraft
        if SaveAsDraft == '1':
            service.save_as_draft = True

        service.save()

        if not SaveAsDraft == '1':
            wait_for_accept = WaitArticlesForAccept.objects.create(service=service, publish_date=timezone.now())
            wait_for_accept.save()

            if language == 'ar':
                messages.success(request, 'طلبك قيد المراجعة سوف يتم نشر خدمتك بعد المراجعة')
            else:
                messages.success(request, 'Your application is under review Your service will be posted after review')

        else:
            if language == 'ar':
                messages.success(request, 'تم حفظ الخدمة كمسودة')
            else:
                messages.success(request, 'The service has been saved as a draft')
        return redirect('myArticles', service.blogTypes.id)
    return render(request, 'dashboard/blog/AddNewArticleForMe.html', {'form':form, 'service_type':service_types, 'download_size_type_list':download_size_type_list})









def EditArticleForMe(request, service_id):
    language = get_language()
    form = AddNewServiceForMeForm
    service = None
    edited_service_is_exists =None
    if request.user.is_superuser:
        service = Article.objects.get(id=service_id)
        edited_service = EditedArticlesWaitForAccept.objects.filter(service=service)
    else:
        service = Article.objects.get(id=service_id, user=request.user)
        edited_service = EditedArticlesWaitForAccept.objects.filter(user=request.user, service=service)

    edited_service_is_exists = edited_service.exists()

    service_model = service
    if edited_service_is_exists:
        service = edited_service[0]
        service_model = service.service

    # get service data from database
    title_ar = service.title_ar
    desc_ar = service.desc_ar
    content_ar = service.article_ar
    keyword_ar = service.keyword_ar
    title_en = service.title_en
    desc_en = service.desc_en
    content_en = service.article_en
    keyword_en = service.keyword_en
    service_type = service.article_Type
    image = service.article_img
    SaveAsDraft = service.save_as_draft

    service_types = ArticleTypes.objects.filter(blog = service_model.blogTypes)

    obj = {
        'title_ar': title_ar,
        'desc_ar': desc_ar,
        'content_ar': content_ar,
        'keyword_ar': keyword_ar,
        'title_en': title_en,
        'desc_en': desc_en,
        'content_en': content_en,
        'keyword_en': keyword_en,
        'service_type': service_type.all(),
        'image': image,
        'SaveAsDraft': SaveAsDraft,
        'service_types': service_types,
        'form':form,
    }

    #set SaveAsDraft to num
    if obj['SaveAsDraft'] == True:
        obj['SaveAsDraft'] = '1'
    else:
        obj['SaveAsDraft'] = '0'

    if request.method == 'POST':
        #get requested data
        title_ar = request.POST.get('title_ar')
        desc_ar = request.POST.get('desc_ar')
        content_ar = request.POST.get('content_ar')
        keyword_ar = request.POST.get('keyword_ar')
        title_en = request.POST.get('title_en')
        desc_en = request.POST.get('desc_en')
        content_en = request.POST.get('content_en')
        keyword_en = request.POST.get('keyword_en')
        service_type = request.POST.getlist('service_type')
        image = request.FILES.get('image')
        SaveAsDraft = request.POST.get('SaveAsDraft')

        

        #delete all avarible edited service for create new one
        if edited_service.exists():
            for i in edited_service:
                i.delete()

        # set SaveAsDraft
        if SaveAsDraft == '1':
            service = Article.objects.get(id=service_model.id)

            service.save_as_draft = True
            service.is_enabled = False
            
            service.title_ar = title_ar
            service.desc_ar = desc_ar
            service.article_ar = content_ar
            service.keyword_ar = keyword_ar
            service.title_en = title_en
            service.desc_en = desc_en
            service.article_en = content_en
            service.keyword_en = keyword_en
            service.article_Type.set(ArticleTypes.objects.filter(id__in=service_type))

            #set image desc 
            service.img_desc_ar = title_ar
            service.img_desc_en = title_en

            #set image if exists
            if image:
                service.article_img = image
            if language == 'ar':
                messages.success(request, 'تم حفظ الخدمة كمسودة')
            else:
                messages.success(request, 'The service has been saved as a draft')

            service.save()
        else:

            if language == 'ar':
                messages.success(request, 'طلبك قيد المراجعة سوف يتم نشر خدمتك بعد المراجعة')
            else:
                messages.success(request, 'Your application is under review Your service will be posted after review')


            messages.success(request, '')
            edited_service_create = EditedArticlesWaitForAccept.objects.create(user=request.user, service=service_model)

            
            edited_service_create.title_ar = title_ar
            edited_service_create.desc_ar = desc_ar
            edited_service_create.article_ar = content_ar
            edited_service_create.keyword_ar = keyword_ar
            edited_service_create.title_en = title_en
            edited_service_create.desc_en = desc_en
            edited_service_create.article_en = content_en
            edited_service_create.keyword_en = keyword_en
            edited_service_create.article_Type.set(ArticleTypes.objects.filter(id__in=service_type))

            #set image desc 
            edited_service_create.img_desc_ar = title_ar
            edited_service_create.img_desc_en = title_en

            #set image if exists
            if image:
                edited_service_create.article_img = image
                

            edited_service_create.save()


        return redirect('myArticles', service_model.blogTypes.id)

    return render(request, 'dashboard/blog/EditArticleForMe.html', obj)



def DeleteMyArticle(request, id):
    article = Article.objects.filter(id=id, user=request.user)[0]
    article.delete()
    return redirect('myArticles', article.blogTypes.id)



def requestsUnderReviewAreticls(request):
    wait_for_accept = WaitArticlesForAccept.objects.all()

    return render(request, 'dashboard/admin/requests_under_review_article.html', {'wait_for_accept':wait_for_accept})



def requestsUnderReviewAreticlsAccept(request, WaitForAcceptID):
    wait_for_accept = WaitArticlesForAccept.objects.get(id=WaitForAcceptID)
    service = wait_for_accept.service
    service.is_enabled = True
    service.save()
    wait_for_accept.delete()
    
    #get service link
    
    service_link = f'/blog/Article/{service.id}'
    #send Notification
    notif_msg_ar = f"""
    <p dir='rtl'>تهانينا تم قبول خدمتك "{service.title}" لمشاهدتها <a style="color: #438fff;" href='{service_link}' target='_blank'>اضغط هنا</a></p>
    """
    notif_msg_en = f"""
    <p dir='rtl'>Congratulations, your service "{service.title}" has been accepted, to view it <a style="color: #438fff;" href='{service_link}' target='_blank'>click here</a></p>
    """
    notif = Notification.objects.create(sender=request.user,receiver=service.user)
    notif.message_en = notif_msg_en
    notif.message_ar = notif_msg_ar
    userprofile = service.user.userprofile
    userprofile.is_not_read_notification = True
    userprofile.save()
    notif.save()

    return redirect('requestsUnderReviewAreticls')



def requestsUnderReviewAreticlsCancel(request, WaitForAcceptID):
    if request.method == 'POST':
        msg = request.POST.get('msg')
        wait_for_accept = WaitArticlesForAccept.objects.get(id=WaitForAcceptID)
        service = wait_for_accept.service
        service.is_enabled = False
        service.save_as_draft = True
        service.save()
        wait_for_accept.delete()

        msg = str(msg).format(username=service.user.username, title=service.title, id=service.id)
        notif = Notification.objects.create(sender=request.user,receiver=service.user)
        notif.message_en = tss.google(msg, to_language='en')
        notif.message_ar = tss.google(msg, to_language='ar')
        userprofile = service.user.userprofile
        userprofile.is_not_read_notification = True
        userprofile.save()
        notif.save()
        return redirect('requestsUnderReviewAreticls')




def requestsUnderReviewEditedAreticls(request):
    wait_for_accept = EditedArticlesWaitForAccept.objects.filter(modification_cancelled=False)

    return render(request, 'dashboard/admin/requests_under_review_edited_article.html', {'wait_for_accept':wait_for_accept})



def requestsUnderReviewEditedAreticlsAccept(request, WaitForAcceptID):
    wait_for_accept = EditedArticlesWaitForAccept.objects.get(id=WaitForAcceptID)
    service = wait_for_accept.service

    # get edited data from database
    title_ar = wait_for_accept.title_ar
    desc_ar = wait_for_accept.desc_ar
    content_ar = wait_for_accept.article_ar
    keyword_ar = wait_for_accept.keyword_ar
    title_en = wait_for_accept.title_en
    desc_en = wait_for_accept.desc_en
    content_en = wait_for_accept.article_en
    keyword_en = wait_for_accept.keyword_en
    service_type = wait_for_accept.article_Type
    image = wait_for_accept.article_img


    # set service data to edited data
    service.title_ar = title_ar
    service.desc_ar = desc_ar
    service.article_ar = content_ar
    service.keyword_ar = keyword_ar
    service.title_en = title_en
    service.desc_en = desc_en
    service.article_en = content_en
    service.keyword_en = keyword_en
    service.article_Type.set(service_type.all())
    if image:
        service.article_img = image

    service.save()

    service.is_enabled = True
    service.save_as_draft = False
    service.save()
    wait_for_accept.delete()



    #get service link
    
    service_link = f'/blog/Article/{service.id}'
    #send Notification
    notif_msg_ar = f"""
        <p dir = 'rtl'> تهانينا ، تم الموافقة على التعديل الذي أجريته على خدمتك "{service.title}" لعرض <a style="color: #438fff;" href='{service_link}' target='_ blank'> انقر هنا </a> </p>
    """
    notif_msg_en = f"""
        <p dir='rtl'>Congratulations, your edit to your service "{service.title}" has been accepted for viewing <a style="color: #438fff; text-decoration: underline;" href='{service_link}' target='_blank'>Click here</a></p>
    """
    notif = Notification.objects.create(sender=request.user,receiver=service.user)
    notif.message_en = notif_msg_en
    notif.message_ar = notif_msg_ar
    userprofile = service.user.userprofile
    userprofile.is_not_read_notification = True
    userprofile.save()
    notif.save()


    return redirect('requestsUnderReviewEditedAreticls')



def requestsUnderReviewEditedAreticlsCancel(request, WaitForAcceptID):
    if request.method == 'POST':
        msg = request.POST.get('msg')
        wait_for_accept = EditedArticlesWaitForAccept.objects.get(id=WaitForAcceptID)
        wait_for_accept.modification_cancelled = True
        wait_for_accept.save()


        msg = str(msg).format(username=wait_for_accept.user.username, title=wait_for_accept.title, id=wait_for_accept.id)
        notif = Notification.objects.create(sender=request.user,receiver=wait_for_accept.user)
        notif.message_en = tss.google(msg, to_language='en')
        notif.message_ar = tss.google(msg, to_language='ar')
        userprofile = wait_for_accept.user.userprofile
        userprofile.is_not_read_notification = True
        userprofile.save()
        notif.save()
    return redirect('requestsUnderReviewEditedAreticls')

def Settings(request):
    user = request.user
    userprofile = user.userprofile
    user_form = UserForm(instance=user)
    userprofile_form = UserProfileForm(instance=userprofile)
    sex = userprofile.sex
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        userprofile_form = UserProfileForm(request.POST, instance=userprofile)
        
        user_form.save()
        userprofile_form.save()
        sex = request.user.userprofile.sex
    return render(request, 'dashboard/account/Settings.html', {'user_form':user_form, 'userprofile_form':userprofile_form, 'sex':sex})


