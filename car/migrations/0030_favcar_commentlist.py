# Generated by Django 3.2.5 on 2021-09-30 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0029_auto_20210930_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='favcar',
            name='commentList',
            field=models.ManyToManyField(blank=True, related_name='favCarCommentItems', to='car.Comment'),
        ),
    ]