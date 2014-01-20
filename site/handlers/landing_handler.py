# -*- coding: utf-8 -*-

from main_handler import MainHandler

class LandingHandler(MainHandler):

    def get(self):
        self.render('landing.html')
