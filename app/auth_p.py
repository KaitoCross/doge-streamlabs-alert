# coding: utf-8

# hash example
"""
hash_object = hashlib.sha1(b'Hello World')
hex_dig = hash_object.hexdigest()
print(hex_dig)
"""

from .database import DB_cl
from threading import Semaphore
import requests, cherrypy
from requests_oauthlib import OAuth2Session

class auth(object):
    exposed = True  # gilt für alle Methoden

    def __init__(self, db):
        #self.sem = Semaphore()
        self.db_o = db #DB_cl(self.sem)
        self.api_base = "https://streamlabs.com/api/v1.0"
        tokens = self.db_o.read("tokens.json")
        auth_dict = {
            'grant_type': 'authorization_code',
            'client_id': tokens['client_id'],
            'client_secret': tokens['client_secret'],
            'redirect_uri': tokens['redirect_uri']
        }
        scope = ['donations.create',
                 'donations.read',
                 'alerts.create']
        self.oauth = OAuth2Session(auth_dict["client_id"], redirect_uri=auth_dict["redirect_uri"], scope=scope)
        self.authorization_url, self.state = self.oauth.authorization_url(
            'https://www.streamlabs.com/api/v1.0/authorize')

    # -------------------------------------------------------
    def GET(self):
        raise cherrypy.HTTPRedirect(self.authorization_url)
        return