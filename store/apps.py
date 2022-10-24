from django.apps import AppConfig
from modeltranslation import settings

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
    # Add Wagtail defined fields as modeltranslation custom fields
    setattr(settings, 'CUSTOM_FIELDS', getattr(settings, 'CUSTOM_FIELDS', ()) + (
        'StreamField', 'RichTextField', 'FroalaField'))