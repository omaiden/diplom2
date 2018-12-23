# Generated by Django 2.1.4 on 2018-12-23 19:41

import datetime
from django.db import migrations, models
import find.models


class Migration(migrations.Migration):

    dependencies = [
        ('find', '0005_auto_20181223_0248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missing_person',
            name='image',
            field=models.ImageField(default='images/non.png', upload_to=find.models.PathAndRename('E:\\python\\diplom2\\diplom2\\images/missing')),
        ),
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 23, 22, 41, 44, 809821)),
        ),
        migrations.AlterField(
            model_name='victim',
            name='image',
            field=models.ImageField(default='images/non.png', upload_to='victim'),
        ),
    ]