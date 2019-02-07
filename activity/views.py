# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from models import User, Activity
from responses import Response
from utils import check_mandatory_fields
from constants import CREATE_ACTIVITY_KEY


# Create your views here.
def create_activity(request):
    try:
        # to put it  into queue or something when running this
        if request.method == "POST":
            post_data = json.loads(request.body)
            if not check_mandatory_fields(post_data, CREATE_ACTIVITY_KEY):
                return Response(402).resp()
            post_data['actor'] = User.objects.get(name=post_data['actor'])
            if post_data['target']:
                post_data['target'] = User.objects.get(name=post_data['target'])
            Activity.objects.create(**post_data)
            return Response(200).resp()
        else:
            return Response(405).resp()
    except Exception as e:
        return Response(500).resp()


def create_user(request):
    try:
        if request.method == "POST":
            post_data = json.loads(request.body)
            User.objects.create(name=post_data['name'])
            return Response(200).resp()
        else:
            return Response(405).resp()
    except Exception as e:
        return Response(500).resp()

