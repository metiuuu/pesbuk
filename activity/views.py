# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ast
import json

from django.db import IntegrityError

from activity.constants import GET_FEED_PARAM_KEY, URL
from constants import CREATE_ACTIVITY_KEY, GET_FEED_BODY_KEY
from models import User, Activity, FriendShip
from responses import Response
from utils import check_mandatory_fields


def create_friendship(request):
    try:
        if request.method == 'POST':
            post_data = json.loads(request.body)
            actor_name = request.GET.get('actor')

            actor_user_id = User.objects.filter(name=actor_name).values_list('pk', flat=True)
            if actor_user_id:
                actor_user_id = actor_user_id[0]

            target_name = post_data.get('follow') if post_data.get('follow') else post_data.get('unfollow')
            friend_id = User.objects.filter(name=target_name).values_list('pk', flat=True)
            if friend_id:
                friend_id = str(friend_id[0])

            if not friend_id or not actor_user_id:
                return Response(400).resp()

            friendship_obj, created = FriendShip.objects.get_or_create(actor_id=actor_user_id)

            if post_data.get('follow'):
                list_of_friend_id = ast.literal_eval(friendship_obj.friend_ids)

                if friend_id in list_of_friend_id:
                    data = {'message': '{target} already in {user} friend list'.format(target=target_name, user=actor_name)}
                    return Response(200).resp(data)
                else:
                    if not list_of_friend_id:
                        data = [friend_id]
                    else:
                        list_of_friend_id.append(friend_id)
                        data = set(list_of_friend_id)
                    friendship_obj.friend_ids = list(data)
                    friendship_obj.save()
                    data = {'message': '{target} are now friend with {user}'.format(target=target_name, user=actor_name)}
                    return Response(200).resp(data)

            elif post_data.get('unfollow'):

                if friendship_obj.friend_ids:
                    list_of_friend_id = ast.literal_eval(friendship_obj.friend_ids)

                    if friend_id in list_of_friend_id:
                        list_of_friend_id.remove(friend_id)
                        friendship_obj.friend_ids = list_of_friend_id
                        friendship_obj.save()
                        data = {'message': '{target} are now no longer {user} friend'.format(target=target_name, user=actor_name)}
                    else:
                        data = {'message': '{target} are not in {user} friend list'.format(target=target_name, user=actor_name)}
                    return Response(200).resp(data)
                return Response(400).resp()
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
                actor_id = User.objects.filter(name=post_data['actor']).values_list('pk', flat=True)
                friend_ids = FriendShip.objects.filter(actor_id=actor_id).values_list('friend_ids', flat=True)
                if friend_ids:
                    pass
                else:
                    data = {'message': 'user does not have any friend yet.'}
            else:
                return Response(400).resp()
        else:
            return Response(405).resp()
    except Exception as e:
        return Response(500).resp()


def create_activity(request):
    try:
        # to put it into queue or something when running this. i would love to explore using aws lambda for this case
        # if possible, need to do POC first else ill use aws sqs for this ,ill create producer method here then ill
        # create a consumer to consume the msg in batches. For now ill just KISS it.
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
        # thinking about to use threading to create user or as above can use producer and consumer as well number of
        # user records might grow to millions and from my limited experience we might not be able to directly
        # archiving user records ,unless the users are no longer activated or closed their account. Anyway ill alway
        # try to KISS (Keep It Simple Stupid) until we really need to change it because of some bottleneck in the
        # future
        if request.method == "POST":
            post_data = json.loads(request.body)
            if not check_mandatory_fields(post_data, ['name']):
                return Response(400).resp()
            User.objects.create(name=post_data['name'])
            return Response(200).resp()
        else:
            return Response(405).resp()
    except IntegrityError as e:
        return Response(200).resp()
    except Exception as e:
        return Response(500).resp()
