# Generated by Django 3.2.5 on 2021-10-07 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0031_view'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='banned',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
