# Generated by Django 3.2.5 on 2021-09-14 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0008_user_favlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='details',
            field=models.CharField(blank=True, default='', max_length=10485759),
        ),
    ]