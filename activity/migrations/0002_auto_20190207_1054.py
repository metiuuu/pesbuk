# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-07 10:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]