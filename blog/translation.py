from .models import Article, ArticleTypes, blogTypes 
from modeltranslation.translator import TranslationOptions,register


@register(Article)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'desc', 'img_desc', 'article', 'keyword')


@register(ArticleTypes)
class ArticleTypesTranslationOptions(TranslationOptions):
    fields = ('name', 'desc', 'img_desc', 'keyword')

@register(blogTypes)
class blogTypesTranslationOptions(TranslationOptions):
    fields = ('name', 'desc', 'img_desc', 'keyword')