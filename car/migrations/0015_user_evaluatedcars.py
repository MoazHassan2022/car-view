# Generated by Django 3.2.5 on 2021-09-16 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0014_auto_20210916_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='evaluatedCars',
            field=models.ManyToManyField(blank=True, related_name='carItems', to='car.Car'),
        ),
    ]
