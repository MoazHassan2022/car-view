# Generated by Django 3.2.5 on 2021-09-24 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0018_ad_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='motorSt',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]