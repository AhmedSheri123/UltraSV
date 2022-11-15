from .models import ConvertImageFormatModel, ToolsModel
from modeltranslation.translator import TranslationOptions,register


@register(ToolsModel)
class ToolsModelTranslationOptions(TranslationOptions):
    fields = ('name', 'desc', 'img_desc', 'keyword')

@register(ConvertImageFormatModel)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'desc', 'image', 'article', 'keyword')
