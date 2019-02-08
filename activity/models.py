# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)


class Activity(models.Model):
    actor_id = models.IntegerField(null=False)
    verb = models.CharField(max_length=256, null=False)
    object = models.CharField(max_length=256, null=True)
    target_id = models.IntegerField(null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)


class FriendShip(models.Model):
    actor_id = models.IntegerField(null=False, unique=True)
    friend_ids = models.TextField(null=False)
    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)

