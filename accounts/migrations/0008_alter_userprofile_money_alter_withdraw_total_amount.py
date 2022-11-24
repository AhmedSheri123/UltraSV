# Generated by Django 4.1.3 on 2022-11-23 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_withdraw_options_alter_userprofile_money_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='money',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=6, null=True, verbose_name='الرصيد'),
        ),
        migrations.AlterField(
            model_name='withdraw',
            name='total_amount',
            field=models.DecimalField(decimal_places=3, max_digits=6, verbose_name='كمية السحب'),
        ),
    ]
