# Generated by Django 4.0 on 2022-11-17 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_alter_services_issued'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='issued',
            field=models.DateField(blank=True, null=True, verbose_name='تاريخ الاصلي التي  نشرت لاول مرة على الانترنت'),
        ),
    ]
