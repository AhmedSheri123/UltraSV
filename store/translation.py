from .models import StoreTypes, ServiceTypes, Services
from modeltranslation.translator import TranslationOptions,register


@register(Services)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'desc', 'img_desc', 'article', 'keyword')


@register(ServiceTypes)
class ArticleTypesTranslationOptions(TranslationOptions):
    fields = ('name', 'desc', 'img_desc', 'keyword')

@register(StoreTypes)
class blogTypesTranslationOptions(TranslationOptions):
    fields = ('name', 'desc', 'img_desc', 'keyword')