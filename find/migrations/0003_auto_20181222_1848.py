# Generated by Django 2.1.4 on 2018-12-22 15:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('find', '0002_auto_20181222_1847'),
    ]

    operations = [
        migrations.RenameField(
            model_name='victim',
            old_name='post1',
            new_name='post',
        ),
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 22, 18, 48, 36, 304619)),
        ),
    ]