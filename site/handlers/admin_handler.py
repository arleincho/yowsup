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
            
        ns.update({
            'q': '',
            'setting': get_setting
        })

        return ns

    def get_current_user(self):
        user = self.get_secure_cookie("userEasyMarketing")
        if user is None:
            return None
        return user
        print utils.check_hash('self.get_argument("password")', password)
        # try:
        #     return user[0]
        # except IndexError:
        #     return None

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



class ChannelsHanlder(AdminHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('admin/channels/index.html')



class LoginHandler(MainHandler):

    def get(self):
        self.render('login.html')

    def post(self):
        password = utils.make_hash(self.get_argument("password"))
        print len(password)
        self.set_secure_cookie("userEasyMarketing", self.get_argument("username"))
        self.redirect("/admin")



class LogoutHandler(MainHandler):

    def get(self):
        self.clear_all_cookies()
        self.redirect(self.reverse_url('login'))