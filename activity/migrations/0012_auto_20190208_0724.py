# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-08 07:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0011_auto_20190208_0717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='target_id',
            field=models.IntegerField(null=True),
        ),
    ]
