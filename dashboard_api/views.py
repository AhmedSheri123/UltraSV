from rest_framework.decorators import  permission_classes
from rest_framework.response import Response
from rest_framework import permissions
# Create your views here.
from store.models import ServiceViews, Services
from blog.models import ArticleViews, Article
from accounts.models import Notification, UserProfile
from rest_framework.views import APIView
from dashboard.countrys import get_location
from django.utils import timezone
from store.views import getMonyByCountry
import hashlib
from django.middleware.csrf import get_token
@permission_classes((permissions.AllowAny,))
#@api_view(['GET', 'POST'])
class SnippetList(APIView):
    def get(self, request, *args, **kwargs):
        lang = request.GET.get('lang')
        direction = request.GET.get('dir')
        objects = {}

        notification = Notification.objects.filter()

        if direction == '0':
            notification = notification.filter(receiver=request.user, is_seen=False)
            
            if notification.exists():
                all_messages = notification.values()
                sender = ''
                publish_date = ''
                for messages in all_messages:
                    notif = Notification.objects.get(id=messages['id'])
                    if lang == 'ar':
                        sender = 'مشرف'
                        publish_date = notif.LastUpdateAR()
                    else:
                        sender = 'Admin'
                        publish_date = notif.LastUpdateEN()
                    if not notif.sender.is_superuser:
                        sender = notif.sender.username
                    messages['sender'] = sender
                    messages['publish_date'] = publish_date

                objects['lastMsg'] = {
                    'is_exists':True,
                    'all_messages':all_messages
                    }


                for i in notification:
                    i.is_seen = True
                    i.save()
                return Response(objects, status=200)
            else:
                objects['lastMsg'] = {
                    'is_exists':False,
                }
        elif direction == '1':
            user = request.user
            userprofile= UserProfile.objects.get(user=user)
            userprofile.is_not_read_notification = False
            userprofile.save()

        objects['is_not_read_notification'] = request.user.userprofile.is_not_read_notification,

        return Response(objects, status=200)



    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''



def addStoreVisitedItem(service, request):
    ip_address = '122.169.13.83'# get_client_ip(request)

    obj = ServiceViews.objects.filter(ip_address=ip_address, visited_date__date=timezone.now().date())
    
    if not obj.exists():
        data = get_location(ip_address)
        country_code=data.get('country_code')
        
        obj = obj.create(ip_address=ip_address, service=service, country_code=country_code, country_name=data.get('country_name'), city=data.get('city'), region=data.get('region'), earn_count=getMonyByCountry(country_code))
        obj.save()
        userprofile = obj.service.user.userprofile
        userprofile.money += obj.earn_count
        userprofile.save()

        return True
    return False


def addBlogVisitedItem(article, request):
    ip_address = '122.169.13.83'# get_client_ip(request)
    obj = ArticleViews.objects.filter(ip_address=ip_address, visited_date__date=timezone.now().date())
    if not obj.exists():
        data = get_location(ip_address)
        country_code=data.get('country_code')

        obj = obj.create(ip_address=ip_address, article=article, country_code=country_code, country_name=data.get('country_name'), city=data.get('city'), region=data.get('region'), earn_count=getMonyByCountry(country_code))
        obj.save()
        userprofile = obj.article.user.userprofile
        userprofile.money += obj.earn_count
        userprofile.save()
        
        return True
    return False

@permission_classes((permissions.AllowAny,))
#@api_view(['GET', 'POST'])
class getViews(APIView):

    def post(self, request, *args, **kwargs):
        data = request.POST
        id = data.get('id')
        direction = data.get('dir')
        csrf = data.get('csrf')
        requested_csrf_md5 = data.get('z-index-ctx')
        
        csrf_md5 = hashlib.md5((csrf+'askdaskkldakl').encode('utf-8')).hexdigest()

        if requested_csrf_md5 == csrf_md5:
            
            if direction == '1':
                article = Article.objects.get(id=id)
                addBlogVisitedItem(article, request)

            if direction == '2':
                service = Services.objects.get(id=id)
                addStoreVisitedItem(service, request)
        return Response({'status':'error to get image'}, status=404)

    # def get(self, request, *args, **kwargs):
        

