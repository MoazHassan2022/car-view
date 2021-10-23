# Generated by Django 3.2.5 on 2021-09-30 17:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0024_auto_20210930_1406'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavCar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=1000)),
                ('image', models.CharField(blank=True, default='', max_length=10485759)),
                ('logo', models.CharField(blank=True, default='', max_length=10485759)),
                ('carID', models.IntegerField(blank=True, default=0, null=True)),
                ('commentList', models.ManyToManyField(blank=True, related_name='favCommentItems', to='car.Comment')),
                ('likes', models.ManyToManyField(blank=True, related_name='carLikesUsers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]