# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import ast

from django.db import IntegrityError

from activity.constants import GET_FEED_PARAM_KEY, URL
from constants import CREATE_ACTIVITY_KEY, GET_FEED_BODY_KEY
from models import User, Activity, FriendShip
from responses import Response
from utils import check_mandatory_fields


# Create your views here.
def friendship(request):
    try:
        if request.method == 'POST':
            post_data = json.loads(request.body)
            actor = request.GET.get('actor')
            actor_user_id = User.objects.filter(name=actor).values_list('pk', flat=True)
            if actor_user_id:
                actor_user_id = actor_user_id[0]
            target_user_id = User.objects.filter(name=post_data.get('follow') if post_data.get('follow') else post_data.get('unfollow')).values_list('pk', flat=True)
            if target_user_id:
                target_user_id = str(target_user_id[0])
            if not target_user_id or not actor_user_id:
                return Response(400).resp()

            friendship_obj, created = FriendShip.objects.get_or_create(actor_id=actor_user_id)

            if post_data.get('follow'):
                # do follow friend here
                target_ids = ast.literal_eval(friendship_obj.target_ids)
                if target_user_id in target_ids:
                    return Response(200).resp()
                else:
                    if not target_ids:
                        data = [target_user_id]
                    else:
                        target_ids.append(target_user_id)
                        data = set(target_ids)
                    friendship_obj.target_ids = list(data)
                    friendship_obj.save()
                    return Response(200).resp()
            elif post_data.get('unfollow'):
                # do unfollow code here
                if friendship_obj.target_ids:
                    target_ids = ast.literal_eval(friendship_obj.target_ids)
                    if target_user_id in target_ids:
                        target_ids.remove(target_user_id)
                        friendship_obj.target_ids = target_ids
                        friendship_obj.save()
                return Response(200).resp()

            else:
                return Response(400).resp()
        else:
            return Response(405).resp()
    except Exception as e:
        return Response(500).resp()


def get_feed(request):
    try:
        if request.method == "POST":
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
