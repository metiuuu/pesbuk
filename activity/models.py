# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50, null=False)
    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'


class Activity(models.Model):
    actor = models.ForeignKey(User, related_name='actor_id')
    verb = models.CharField(max_length=256, null=False)
    object = models.CharField(max_length=256, null=True)
    target = models.ForeignKey(User, null=True, related_name='target_id')
    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'activity'
