# Generated by Django 3.2.5 on 2021-10-16 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0033_ad_carid'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='image1',
            field=models.CharField(blank=True, default='', max_length=10485759),
        ),
        migrations.AddField(
            model_name='ad',
            name='image2',
            field=models.CharField(blank=True, default='', max_length=10485759),
        ),
        migrations.AddField(
            model_name='ad',
            name='image3',
            field=models.CharField(blank=True, default='', max_length=10485759),
        ),
        migrations.AddField(
            model_name='ad',
            name='image4',
            field=models.CharField(blank=True, default='', max_length=10485759),
        ),
    ]
