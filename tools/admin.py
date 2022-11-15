from django.contrib import admin
from .models import ConvertImageFormatModel, ToolsModel, convertedImageDeleteTask
from modeltranslation.admin import TranslationAdmin
# Register your models here.
admin.site.register(convertedImageDeleteTask)

@admin.register(ToolsModel)
class ToolsModelAdmin(TranslationAdmin):
    list_display = ('name',)
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css','https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'),
            
        }

@admin.register(ConvertImageFormatModel)
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