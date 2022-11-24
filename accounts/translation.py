from .models import Notification
from modeltranslation.translator import TranslationOptions,register


@register(Notification)
class NotificationTranslationOptions(TranslationOptions):
    fields = ('message',)
