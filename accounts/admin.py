from django.contrib import admin
from .models import UserProfile, Notification, Withdraw, VerifiedEmail
from modeltranslation.admin import TranslationAdmin
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Withdraw)
admin.site.register(VerifiedEmail)

@admin.register(Notification)
class NotificationAdmin(TranslationAdmin):
    list_display = ('id', 'sender' ,'receiver')
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css','https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'),
            
        }