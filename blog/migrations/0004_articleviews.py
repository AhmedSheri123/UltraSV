# Generated by Django 4.1.2 on 2022-10-22 23:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_article_last_update'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleViews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('visited_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.article', verbose_name='الخدمة')),
            ],
        ),
    ]