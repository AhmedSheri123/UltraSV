# Generated by Django 4.1.3 on 2022-11-20 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0030_alter_serviceviews_country_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceviews',
            name='earn_count',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='ربحت من الزيارة'),
        ),
    ]
