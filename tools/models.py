from django.db import models
from froala_editor.fields import FroalaField
# Create your models here.

IMAGE_FORMAT_CHOICES = (
    ("png", "png"),
    ("jpg", "jpg"),
    ("webp", "webp"),
    ("ico", "ico"),
    ("pdf", "pdf"),
)

TOOLS_URL_CHOICES = (
    ("AllConvertImageFormatToAnother", "AllConvertImageFormatToAnother"),
)


class ToolsModel(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم المتجر")
    desc = models.TextField(verbose_name="وصف", null=True, blank=True)
    img = models.ImageField(upload_to='blogTypes/img/', null=True, blank=True)
    img_desc = models.CharField(max_length=255, verbose_name="وصف الصورة", null=True, blank=True)
    keyword = models.TextField(verbose_name="كلمات مفتاحية", null=True, blank=True)
    redirect_url = models.CharField(choices=TOOLS_URL_CHOICES, default="AllConvertImageFormatToAnother", max_length=255, unique=True, verbose_name="اسم العنوان الذي تريد التوجه عليه")
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class ConvertImageFormatModel(models.Model):
    title = models.CharField(max_length=255, verbose_name="العنوان")
    desc = models.TextField(verbose_name="الوصف", blank=True)
    image = models.ImageField(upload_to="tools/ConvertImageFormatToImage/", verbose_name="الصورة", blank=True)
    from_format = models.CharField(max_length=50, choices=IMAGE_FORMAT_CHOICES, default="png")
    to_format = models.CharField(max_length=50, choices=IMAGE_FORMAT_CHOICES, default="jpg")
    article = FroalaField(verbose_name="المقالة", blank=True)
    keyword = models.TextField(verbose_name="كلمات مفتاحية", null=True, blank=True)


class convertedImageDeleteTask(models.Model):
    path = models.CharField(max_length=255, verbose_name="مسار الملف")
    is_deleted = models.BooleanField(default=False)
    delete_date_time = models.DateTimeField(verbose_name="تاريخ الحذف")

    def __str__(self):
        return self.path


