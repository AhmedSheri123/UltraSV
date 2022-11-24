
from django.contrib import admin
from .models import Article, blogTypes, ArticleTypes, ArticleViews, EditedArticlesWaitForAccept, WaitArticlesForAccept
from modeltranslation.admin import TranslationAdmin
# Register your models here.
admin.site.register(ArticleViews)
admin.site.register(WaitArticlesForAccept)

@admin.register(Article)
class ProductAdmin(TranslationAdmin):
    list_display = ('title',)
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css','https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'),
            
        }




@admin.register(EditedArticlesWaitForAccept)
class EditedArticlesWaitForAcceptAdmin(TranslationAdmin):
    list_display = ('id', 'title')
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css','https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'),
            
        }



@admin.register(ArticleTypes)
class ArticleTypesAdmin(TranslationAdmin):
    list_display = ('name',)
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(blogTypes)
class blogTypesAdmin(TranslationAdmin):
    list_display = ('name',)
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }