# -*- coding: utf-8 -*-

from mongoengine import *
from datetime import datetime

channel_list = (
    ('whatsapp', 'WhatsApp'),
    ('sip', 'Sip'),
    ('prerecorded_calls', 'LLamadas Pregrabadas'),
    ('email', 'Email')
)

range_list = (
    ('minute', 'Minutos'),
    ('hour', 'Horas'),
    ('day', 'Diario'),
    ('weekly', 'Semanal'),
)



class User(Document):

    first_name = StringField()
    last_name = StringField()
    username = EmailField(required=True)
    password = StringField(required=True, max_length=69, min_length=69)
    remember = StringField(max_length=80, min_length=80)
    created_at = DateTimeField(default=datetime.now)

    meta = {'collection': 'users'}



class Channel(Document):

    name = StringField(required=True, unique_with=['user'])
    channel_type =  StringField(max_length=17, choices=channel_list)
    config = DictField()
    user = ReferenceField(User)
    created_at = DateTimeField(default=datetime.now)

    meta = {'collection': 'channels'}



class Campaign(Document):
    
    name = StringField(required=True)
    description = StringField(required=True)
    channel = ReferenceField(Channel)
    start_date = DateTimeField(required=True)
    end_date = DateTimeField()
    launch = BooleanField(default=False)
    launch_at_range = StringField(required=True, max_length=6, choices=range_list)
    launch_at_mount = IntField(required=True, min_value=1)
    amount = IntField(required=True, min_value=1)
    user = ReferenceField(User)
    created_at = DateTimeField(default=datetime.now)

    meta = {'collection': 'campaigns'}




class Target(Document):
    
    target = StringField(required=True)
    campaign = ReferenceField(Campaign)
    valid = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)



class Result(Document):

    target = ReferenceField(Target)
    data = DictField()
    created_at = DateTimeField(default=datetime.now)
    meta = {'collection': 'results'}

