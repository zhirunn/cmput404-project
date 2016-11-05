# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-01 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_auto_20161101_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='visibility',
            field=models.CharField(choices=[('PRIVATE', 'PRIVATE'), ('SERVERONLY', 'SERVERONLY'), ('FRIENDS', 'FRIENDS'), ('FOAF', 'FOAF'), ('PUBLIC', 'PUBLIC')], default='0', max_length=1),
        ),
    ]
