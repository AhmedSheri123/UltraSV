
from django import template
from store.models import WaitForAccept, ServiceViews, EditedServicesWaitForAccept
from blog.models import WaitArticlesForAccept, ArticleViews, EditedArticlesWaitForAccept
from accounts.models import Notification

register = template.Library()

@register.simple_tag
def check_if_servies_is_under_review(id):
      obj = WaitForAccept.objects.filter(service__id=id)
      if obj.exists():
            return True
      return False 

@register.simple_tag
def check_if_edited_servies_is_under_review(id):
      obj = EditedServicesWaitForAccept.objects.filter(service__id=id)
      if obj.exists():
            return True
      return False
      
@register.simple_tag
def check_if_edited_servies_is_modification_cancelled(id):
      obj = EditedServicesWaitForAccept.objects.filter(service__id=id, modification_cancelled=True)
      if obj.exists():
            return True
      return False 


@register.simple_tag
def get_Service_watching_count(id):
      watching_count = ServiceViews.objects.filter(service__id=id).count()
      return watching_count








@register.simple_tag
def check_if_article_is_under_review(id):
      obj = WaitArticlesForAccept.objects.filter(service__id=id)
      if obj.exists():
            return True
      return False 

@register.simple_tag
def check_if_edited_article_is_under_review(id):
      obj = EditedArticlesWaitForAccept.objects.filter(service__id=id)
      if obj.exists():
            return True
      return False
      
@register.simple_tag
def check_if_edited_article_is_modification_cancelled(id):
      obj = EditedArticlesWaitForAccept.objects.filter(service__id=id, modification_cancelled=True)
      if obj.exists():
            return True
      return False 


@register.simple_tag
def get_article_watching_count(id):
      watching_count = ArticleViews.objects.filter(article__id=id).count()
      return watching_count








@register.simple_tag
def get_notification(receiver_id):
      notifications = Notification.objects.filter(receiver__id=receiver_id)

      return notifications