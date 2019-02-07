# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import IntegrityError

from activity.constants import GET_FEED_PARAM_KEY, URL
from constants import CREATE_ACTIVITY_KEY, GET_FEED_BODY_KEY
from models import User, Activity
from responses import Response
from utils import check_mandatory_fields


# Create your views here.
def get_feed(request):
    try:
        if request.method == "GET":
            data = dict()
            post_data = json.loads(request.body)
            if not check_mandatory_fields(post_data, GET_FEED_BODY_KEY) or not check_mandatory_fields(request.GET, GET_FEED_PARAM_KEY):
                return Response(400).resp()
            offset = int(request.GET.get('offset'))
            batch_limit = int(request.GET.get('batch_limit'))
            if post_data['friends_feed'] == "na":
                activity_list = Activity.objects.filter(actor__name=post_data['actor'])[offset:batch_limit]
                for rec in activity_list:
                    data['my_feed'] = {'actor': rec.actor.name, 'verb': rec.verb, 'object': rec.object, 'target': rec.target.name, 'datetime': rec.creation_time}
                offset = batch_limit
                batch_limit += batch_limit
                data['next_url'] = URL.format(offset=offset, batch_limit=batch_limit)
                return Response(200).resp(data)
            elif post_data['friends_feed'] == "ya":
                pass
            else:
                return Response(400).resp()
        else:
            return Response(405).resp()
    except Exception as e:
        return Response(500).resp()


def create_activity(request):
    try:
        # to put it  into queue or something when running this
        if request.method == "POST":
            post_data = json.loads(request.body)
            if not check_mandatory_fields(post_data, CREATE_ACTIVITY_KEY):
                return Response(400).resp()
            post_data['actor'] = User.objects.get(name=post_data['actor'])
            if post_data['target']:
                post_data['target'] = User.objects.get(name=post_data['target'])
            Activity.objects.create(**post_data)
            return Response(200).resp()
        else:
            return Response(405).resp()
    except User.DoesNotExist as e:
        return Response(400).resp()
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
    except IntegrityError as e:
        return Response(200).resp()
    except Exception as e:
        return Response(500).resp()
