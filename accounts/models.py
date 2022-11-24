from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import math
from dashboard.countrys import list_of_countrys
from random import choice
from string import ascii_letters


def GenrateString():
    a = ''.join(choice(ascii_letters) for i in range(250))
    return a

# Create your models here.
withdraw_status_list = (
    ('0', 'Pending,, قيد الانتظار'),
    ('1', 'Approved,, وافق'),
    ('2', 'Complete,, مكتمل'),
    ('3', 'Cancelled,, ألغيت'),
)
withdrawal_method_list = (
    ('0','paypal'),
)

sex_chooses = (
    ('male', 'Male'),
    ('female', 'Female')
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='المستخدم')
    sex = models.CharField(choices=sex_chooses, max_length=254, verbose_name='الجنس')
    address = models.CharField( max_length=250, verbose_name="العنوان1", blank=True, null=True)
    address2 = models.CharField( max_length=250, verbose_name="العنوان2", blank=True, null=True)
    city = models.CharField( max_length=250, verbose_name="المدينة", blank=True, null=True)
    state = models.CharField(max_length=250, verbose_name="الولاية", blank=True, null=True)
    zip_code = models.CharField( max_length=250, verbose_name="الرمز البريدي", blank=True, null=True)
    countrys = models.CharField(choices=list_of_countrys, max_length=250, verbose_name="البلد", blank=True, null=True)
    phone_number = models.CharField( max_length=250, verbose_name="رقم الهاتف", blank=True, null=True)
    money = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='الرصيد')
    is_not_read_notification = models.BooleanField(default=False, verbose_name="انه لم يقراء الاشعارات بعد")
    verified_email = models.BooleanField(default=False, verbose_name="هل تم تأكيد الحساب عبر البريد الالكتروني ")


    def __str__(self):
        return self.user.username

class Withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='المستخدم')
    status = models.CharField(choices=withdraw_status_list, max_length=250, verbose_name="الحالة")
    total_amount = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='كمية السحب')
    withdrawal_method = models.CharField(choices=withdrawal_method_list, max_length=250, verbose_name="نوع السحب")
    desc = models.TextField(verbose_name='وصف')
    is_completed = models.BooleanField(default=False, verbose_name='دفعت')
    withdraw_date = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ السحب')


    class Meta:
        ordering = ['-withdraw_date']

    def __str__(self):
        return self.user.username

    def get_status_ar(self):
        for i in withdraw_status_list:
            if i[0] == self.status:
                return i[1].split(',,')[1]

    def get_status_en(self):
        for i in withdraw_status_list:
            if i[0] == self.status:
                return i[1].split(',,')[0]

    def get_withdrawal_method(self):
        for i in withdrawal_method_list:
            if i[0] == self.withdrawal_method:
                return i[1]

class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender', verbose_name='المتلقي')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', verbose_name='المتلقي')
    message = models.TextField(verbose_name='الرسالة')
    is_seen = models.BooleanField(default=False, verbose_name='هل رأى')
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الارسال')

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

class VerifiedEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField(verbose_name='البريد الالكتروني')
    secret = models.CharField(max_length=255, default=GenrateString, verbose_name='كملة سر التأكيد', unique=True)
    is_finshed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class ResetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    secret = models.CharField(max_length=255, default=GenrateString, verbose_name='كملة سر التأكيد', unique=True)
    is_finshed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username