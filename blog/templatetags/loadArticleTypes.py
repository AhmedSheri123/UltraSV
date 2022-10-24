
from django import template
register = template.Library()
    
from ..models import blogTypes
  
@register.simple_tag
def ArticleTypesObjects():
      return blogTypes.objects.all()