from django.db import models
from froala_editor.fields import FroalaField
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



    def __str__(self):
        return self.name
class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان المقالة")
    desc = models.TextField(verbose_name="وصف", null=True)
    article_img = models.ImageField(upload_to='article/img/%Y/%m/%d', null=True)
    img_desc = models.CharField(max_length=255, verbose_name="وصف الصورة", null=True)
    article = FroalaField()
    blogTypes = models.ForeignKey(blogTypes, on_delete=models.CASCADE, verbose_name="نوع المدونة", null=True)
    article_Type = models.ManyToManyField(ArticleTypes, verbose_name="نوع المقالة")
    keyword = models.TextField(verbose_name="كلمات مفتاحية", null=True)
    
    publish_date = models.DateTimeField(auto_now_add=True, null=True)
    last_update = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish_date']

class ArticleViews(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="الخدمة")
    ip_address = models.GenericIPAddressField()
    visited_date = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.article.title