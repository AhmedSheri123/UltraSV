from django.db import models
from froala_editor.fields import FroalaField
from django.utils import timezone
import math
# Create your models here.





class StoreTypes(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم المتجر")
    desc = models.TextField(verbose_name="وصف", null=True, blank=True)
    img = models.ImageField(upload_to='blogTypes/img/', null=True, blank=True)
    img_desc = models.CharField(max_length=255, verbose_name="وصف الصورة", null=True, blank=True)
    keyword = models.TextField(verbose_name="كلمات مفتاحية", null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class ServiceTypes(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم قسم الخدمة")
    store = models.ForeignKey(StoreTypes, on_delete=models.CASCADE, verbose_name="المتجر", null=True)
    desc = models.TextField(verbose_name="وصف", null=True, blank=True)
    img = models.ImageField(upload_to='blogTypes/img/', null=True, blank=True)
    img_desc = models.CharField(max_length=255, verbose_name="وصف الصورة", null=True, blank=True)
    keyword = models.TextField(verbose_name="كلمات مفتاحية", null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name



    def __str__(self):
        return self.name
class Services(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان المقالة")
    desc = models.TextField(verbose_name="وصف", null=True)
    article_img = models.ImageField(upload_to='article/img/%Y/%m/%d', null=True)
    img_desc = models.CharField(max_length=255, verbose_name="وصف الصورة", null=True)
    article = FroalaField()
    storeTypes = models.ForeignKey(StoreTypes, on_delete=models.CASCADE, verbose_name="نوع المتجر", null=True)
    service_Type = models.ManyToManyField(ServiceTypes, verbose_name="نوع الخدمة")
    keyword = models.TextField(verbose_name="كلمات مفتاحية", null=True)
    is_from_url = models.BooleanField(default=False, verbose_name="هل رابط تحميل الخدمة من الخارج")
    service_url = models.CharField(max_length=255, blank=True, verbose_name="رابط الخدمة")
    is_from_local = models.BooleanField(default=False, verbose_name="هل تريد رفع الخدمة محليا")
    is_download_btn_get_without_getDownloadsLink = models.BooleanField(default=False, verbose_name="#btn اذهب الى قطعة من الصفحة مثلا ")
    download_btn_get_without_getDownloadsLink = models.CharField(max_length=255, blank=True, verbose_name="اذهب الى قطعة من الصفحة")
    service_file = models.FileField(upload_to="service/files/%Y/%m/", blank=True, verbose_name='رفع ملف')
    service_version = models.CharField(max_length=255, verbose_name="اصدار الخدمة", null=True, blank=True)
    file_size = models.CharField(max_length=255, verbose_name="حجم الملف المراد تنزيله", null=True, blank=True)
    issued = models.DateTimeField(null=True, verbose_name="تاريخ الاصلي التي  نشرت لاول مرة على الانترنت", blank=True)
    show_download_button = models.BooleanField(default=True, verbose_name="اظهار زر تحميل الخدمة")
    show_contuct_button = models.BooleanField(default=False, verbose_name="اظهار زر التواصل معنا الخدمة")
    is_enabled = models.BooleanField(default=True, verbose_name="هل الخدمة مفعلة ليظهر على الموقع")
    publish_date = models.DateTimeField(auto_now_add=True, null=True)
    last_update = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish_date']




    def __str__(self):
        return self.title


    def LastUpdateEN(self):
        now = timezone.now()
        
        diff= now - self.last_update

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"




    def LastUpdateAR(self):
        now = timezone.now()
        
        diff= now - self.last_update

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return "منذ " + str(seconds) + " ثانية"
            
            else:
                return "منذ " + str(seconds) + " ثواني"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return "منذ " + str(minutes)  + " دقيقة"
            
            else:
                return "منذ " + str(minutes)  + " دقيقة"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return "منذ " + str(hours) + " ساعة"

            else:
                return "منذ " + str(hours) + " ساعات"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return "منذ " + str(days) + " يوم"

            else:
                return "منذ " + str(days) + " ايام"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return "منذ " + str(months) + " شهر"

            else:
                return "منذ " + str(months) + " اشهر"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return "منذ " + str(years) + " سنة"

            else:
                return "منذ " + str(years) + " سنوات"















class ServicesDownloads(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE, verbose_name="الخدمة")
    ip_address = models.GenericIPAddressField()
    downloaded_date = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.service.title
class ServiceViews(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE, verbose_name="الخدمة")
    ip_address = models.GenericIPAddressField()
    visited_date = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.service.title