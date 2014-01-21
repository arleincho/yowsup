# -*- coding: utf-8 -*-

import tornado.web
import utils

from main_handler import MainHandler
from models import *



class AdminHandler(MainHandler):

    def get_template_namespace(self):
        ns = super(MainHandler, self).get_template_namespace()

        def get_setting(setting_name):
            return self.application.settings[setting_name]

        def get_channel_list():
            return channel_list

        def get_channels_active():
            return channel_list_active

        def get_range_list():
            return range_list
            
        ns.update({
            'q': '',
            'setting': get_setting,
            'channel_list': get_channel_list,
            'ranges_list': get_range_list,
            'channels_active': get_channels_active
        })

        return ns

    def get_current_user(self):
        user = self.get_secure_cookie("userEasyMarketing")
        if user:
            user =  User.objects(username=user).first()
            return user
        return None

    @tornado.web.authenticated
    def get(self):
        self.render('admin/index.html')



class CampaignsHanlder(AdminHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('admin/campaigns/index.html')




class CampaignAddHanlder(AdminHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('admin/campaigns/add.html')

    @tornado.web.authenticated
    def post(self):
        self.render('admin/campaigns/add.html')



class ChannelsHanlder(AdminHandler):

    @tornado.web.authenticated
    def get(self):
        channels = Channel.objects(user=self.get_current_user())
        self.render('admin/channels/index.html', channels=channels)



class ChannelAddHanlder(AdminHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('admin/channels/add.html', error="")

    @tornado.web.authenticated
    def post(self):
        channel_type = self.get_arguments('channel_type', None)
        if channel_type:
            data = {}
            data_channel_type = {}
            for attr in self.request.arguments:
                key_channel_type = channel_type[0]
                data_attr = self.get_arguments(attr)
                if attr.startswith(key_channel_type, 0, len(key_channel_type)):
                    if data_attr:
                        data_channel_type.update({attr.split('_', 1)[1]: data_attr[0]})
                else:
                    data.update({attr: data_attr[0]})
            data['config'] = data_channel_type
            data['user'] = self.get_current_user()
            channel = Channel(**data)
            try:
                channel.save()
                self.redirect(self.reverse_url('channels'))
            except NotUniqueError:
                self.render('admin/channels/add.html', error='Ya existe un canal con el mismo nombre')
            except Exception, e:
                self.render('admin/channels/add.html', error='Ocurrio un error al momento de guardar el canal')



class LoginHandler(AdminHandler):

    def get(self):
        if self.get_current_user():
            self.redirect(self.reverse_url('admin'))
        else:
            next_url = self.get_argument('next', '')
            self.render('login.html', error=None, next=next_url)

    def post(self):

        username = self.get_argument('username')
        password = self.get_argument('password')
        next_url = self.get_argument('next', '')

        user =  User.objects(username=username).first()
        if user:

            if utils.check_hash(password, user.password):
                self.set_secure_cookie("userEasyMarketing", self.get_argument("username"))
                self.redirect(next_url or self.reverse_url('admin'))
            else:
                error = 'Incorrecto usuario o password'
                self.render(
                    'login.html',
                    error=error, next_url=next_url)
        else:
            error = 'Incorrecto usuario o password'
            self.render(
                'login.html',
                error=error, next_url=next_url)




class RegisterHandler(AdminHandler):

    def get(self):
        if self.get_current_user():
            self.redirect("/admin")
        else:
            self.render('register.html')

    def post(self):
        data = {}
        for attr in self.request.arguments:
            data_attr = self.get_argument("password", None)
            if data_attr:
                if attr == 'password':
                    data.update({'password': utils.make_hash(self.get_argument("password"))})
                else:
                    data.update({attr: str(self.get_argument(attr))})
        if data:
            user = User(**data)
            user.save()
        self.redirect(self.reverse_url('login'))



class LogoutHandler(AdminHandler):

    def get(self):
        self.clear_all_cookies()
        self.redirect(self.reverse_url('login'))




