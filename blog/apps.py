from django.apps import AppConfig
from modeltranslation import settings

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    # Add Wagtail defined fields as modeltranslation custom fields
    setattr(settings, 'CUSTOM_FIELDS', getattr(settings, 'CUSTOM_FIELDS', ()) + (
        'StreamField', 'RichTextField', 'FroalaField'))