# coding: utf-8

# hash example
"""
hash_object = hashlib.sha1(b'Hello World')
hex_dig = hash_object.hexdigest()
print(hex_dig)
"""

from .database import DB_cl
from threading import Semaphore
import requests
import requests_oauthlib, cherrypy
from requests_oauthlib import OAuth2Session

class oauth(object):
    exposed = True  # gilt für alle Methoden

    def __init__(self,db, alertSender):
        #self.sem = Semaphore()
        self.db_o = db #DB_cl(self.sem)
        self.api_base = "https://streamlabs.com/api/v1.0"
        tokens = self.db_o.read("tokens.json")
        self.auth_dict = {
                'grant_type': 'authorization_code',
                #'code': code,
                'client_id': tokens['client_id'],
                'client_secret': tokens['client_secret'],
                'redirect_uri': tokens['redirect_uri']
                }
        self.scope = ['donations.create',
                 'donations.read',
                 'alerts.create']
        self.oauth = OAuth2Session(self.auth_dict["client_id"], redirect_uri=self.auth_dict["redirect_uri"], scope=self.scope)
        self.alert_sender = alertSender

    # -------------------------------------------------------
    def GET(self, code=None, error=None, error_description = None, state = None):
        print(code)
        retVal_s = "Successful"
        referrer = cherrypy.request.headers.get('Referrer', '/')
        if error_description:
            return error_description
        if code:
            self.auth_dict["code"] = code
            self.auth_dict["tokens"] = self.oauth.fetch_token(
            'https://streamlabs.com/api/v1.0/token',
            code=code,
            client_id=self.auth_dict["client_id"],
            client_secret=self.auth_dict["client_secret"])
            print(self.auth_dict)
            self.db_o.rewrite("tokens.json",self.auth_dict)
            self.alert_sender.load_creds()

        return retVal_s