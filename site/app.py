# -*- coding: utf-8 -*-

import base64
import logging
import os
import sys
import tornado.web
import uuid

from handlers import *
from utils import get_url_spec

path = os.getcwd()
cookie_secret = 'JoHKkDvVT1CKJKjXN514M//RYtPAp0k0rCniY5TxxwU=5234523/(&(/%&/$%·$%'
base_url = ''

settings = {
    "autoescape": None,
    "cookie_secret": cookie_secret,
    "login_url": "/login",
    "template_path": os.path.join(path, "templates"),
    "static_path": os.path.join(path, "static"),
    'base_url': base_url
}

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='"%(asctime)s %(levelname)8s %(name)s - %(message)s"',
    datefmt='%H:%M:%S'
)

U = get_url_spec(base_url)

app = tornado.web.Application([
        U(r"", LandingHandler, name='landig'),
        U(r"admin/?", AdminHandler, name='admin'),
        U(r"admin/campaigns/?", CampaignsHanlder, name='campaigns'),
        U(r"admin/channels/?", ChannelsHanlder, name='channels'),
        U(r"login/?", LoginHandler, name='login'),
        U(r"logout/?", LogoutHandler, name='logout'),
    ],
    debug=True,
    gzip=True,
    **settings
)