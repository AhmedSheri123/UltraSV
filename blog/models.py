from django.db import models
from froala_editor.fields import FroalaField
from django.contrib.auth.models import User
from django.utils import timezone
import math
from dashboard.countrys import list_of_countrys
# Create your models here.




class blogTypes(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم المدونة")
    desc = models.TextField(verbose_name="وصف", null=True, blank=True)
    img = models.ImageField(upload_to='blogTypes/img/', null=True, blank=True)
    img_desc = models.CharField(max_length=255, verbose_name="وصف الصورة", null=True, blank=True)
    keyword = models.TextField(verbose_name="كلمات مفتاحية", null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class ArticleTypes(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم قسم المقالة")
    blog = models.ForeignKey(blogTypes, on_delete=models.CASCADE, verbose_name="المدونة", null=True)
    desc = models.TextField(verbose_name="وصف", null=True, blank=True)
    img = models.ImageField(upload_to='blogTypes/img/', null=True, blank=True)
    img_desc = models.CharField(max_length=255, verbose_name="وصف الصورة", null=True, blank=True)
    keyword = models.TextField(verbose_name="كلمات مفتاحية", null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='الناشر', null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name="عنوان المقالة", blank=True)
    desc = models.TextField(verbose_name="وصف", null=True, blank=True)
    article_img = models.ImageField(upload_to='article/img/%Y/%m/%d', null=True, blank=True)
    img_desc = models.CharField(max_length=255, verbose_name="وصف الصورة", null=True, blank=True)
    article = FroalaField(blank=True)
    blogTypes = models.ForeignKey(blogTypes, on_delete=models.CASCADE, verbose_name="نوع المدونة", null=True, blank=True)
    article_Type = models.ManyToManyField(ArticleTypes, verbose_name="نوع المقالة", blank=True)
    keyword = models.TextField(verbose_name="كلمات مفتاحية", null=True, blank=True)
    publish_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True, null=True, blank=True)

    is_enabled = models.BooleanField(default=True, verbose_name="هل الخدمة مفعلة ليظهر على الموقع")
    save_as_draft = models.BooleanField(default=False, verbose_name="حفظ كمسودة")
    is_visible_to_the_user = models.BooleanField(default=True, verbose_name="اظهار الخدمة عند المستخدم")
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish_date']


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








class EditedArticlesWaitForAccept(models.Model):
    service = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='الخدمة المعدلة')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='الناشر', null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name="عنوان المقالة", blank=True)
    desc = models.TextField(verbose_name="وصف", null=True, blank=True)
    article_img = models.ImageField(upload_to='article/img/%Y/%m/%d', null=True, blank=True)
    img_desc = models.CharField(max_length=255, verbose_name="وصف الصورة", null=True, blank=True)
    article = FroalaField(blank=True)
    blogTypes = models.ForeignKey(blogTypes, on_delete=models.CASCADE, verbose_name="نوع المدونة", null=True, blank=True)
    article_Type = models.ManyToManyField(ArticleTypes, verbose_name="نوع المقالة", blank=True)
    keyword = models.TextField(verbose_name="كلمات مفتاحية", null=True, blank=True)
    save_as_draft = models.BooleanField(default=False, verbose_name="حفظ كمسودة")
    publish_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modification_cancelled = models.BooleanField(default=False, verbose_name="تم الغاء التعديل")


    def __str__(self):
        return self.title + ' id=' + str(self.id)
        
        
    class Meta:
        ordering = ['-publish_date']






    def LastUpdateEN(self):
        now = timezone.now()
        
        diff= now - self.publish_date

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
        
        diff= now - self.publish_date

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














class ArticleViews(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="الخدمة")
    ip_address = models.GenericIPAddressField()
    visited_date = models.DateTimeField(auto_now_add=True, null=True)
    country_code = models.CharField(choices=list_of_countrys, max_length=250, blank=True, null=True)
    country_name = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    region = models.CharField(max_length=250, blank=True, null=True)
    earn_count = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='ربحت من الزيارة', blank=True, null=True)
    
    def __str__(self):
        return self.article.title

class WaitArticlesForAccept(models.Model):
    service = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='الخدمة')
    publish_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.service.title + ' id=' + str(self.service.id)