# Generated by Django 4.0 on 2022-11-17 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_services_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='service_Type',
            field=models.ManyToManyField(to='store.ServiceTypes', verbose_name='نوع الخدمة'),
        ),
    ]
