# Generated by Django 4.1.3 on 2022-11-19 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0009_waitarticlesforaccept'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditedArticlesWaitForAccept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='عنوان المقالة')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='وصف')),
                ('article_img', models.ImageField(blank=True, null=True, upload_to='article/img/%Y/%m/%d')),
                ('img_desc', models.CharField(blank=True, max_length=255, null=True, verbose_name='وصف الصورة')),
                ('article', froala_editor.fields.FroalaField(blank=True)),
                ('keyword', models.TextField(blank=True, null=True, verbose_name='كلمات مفتاحية')),
                ('save_as_draft', models.BooleanField(default=False, verbose_name='حفظ كمسودة')),
                ('publish_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modification_cancelled', models.BooleanField(default=False, verbose_name='تم الغاء التعديل')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.article', verbose_name='الخدمة المعدلة')),
                ('service_Type', models.ManyToManyField(blank=True, to='blog.articletypes', verbose_name='نوع الخدمة')),
                ('storeTypes', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.blogtypes', verbose_name='نوع المتجر')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='الناشر')),
            ],
            options={
                'ordering': ['-publish_date'],
            },
        ),
    ]
