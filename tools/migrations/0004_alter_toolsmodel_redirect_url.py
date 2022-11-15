# Generated by Django 4.1.2 on 2022-10-28 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0003_toolsmodel_convertimageformatmodel_keyword_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolsmodel',
            name='redirect_url',
            field=models.CharField(choices=[('AllConvertImageFormatToAnother', 'AllConvertImageFormatToAnother')], default='AllConvertImageFormatToAnother', max_length=255, unique=True, verbose_name='اسم العنوان الذي تريد التوجه عليه'),
        ),
    ]
