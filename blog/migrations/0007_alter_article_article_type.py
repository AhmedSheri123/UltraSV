# Generated by Django 4.0 on 2022-11-17 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_article_is_enabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_Type',
            field=models.ManyToManyField(to='blog.ArticleTypes', verbose_name='نوع المقالة'),
        ),
    ]
