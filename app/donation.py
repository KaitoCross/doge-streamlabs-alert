# coding: utf-8

import cherrypy
import html
from threading import Semaphore
from requests_oauthlib import OAuth2Session, TokenUpdated

# hash example
"""
hash_object = hashlib.sha1(b'Hello World')
hex_dig = hash_object.hexdigest()
print(hex_dig)
"""

from .database import DB_cl

class Application_cl(object):
    exposed = True  # gilt für alle Methoden
    def __init__(self,db):
        #self.sem = Semaphore()
        self.db_o = db # DB_cl(self.sem)
        self.auth_tokens = {}
        self.load_token()


    def load_token(self):
        self.tokens = self.db_o.read("tokens.json")
        if "tokens" in self.tokens.keys():
            self.auth_tokens = self.tokens["tokens"]
            self.extra = {'client_id': self.tokens['client_id'],
                'client_secret': self.tokens['client_secret'],
                'redirect_uri': self.tokens['redirect_uri']}
        if self.auth_tokens:
            return True
        else:
            return False

    def save_token(self,new_t):
        self.tokens["tokens"] = new_t
        self.auth_tokens = new_t
        self.extra = {'client_id': self.tokens['client_id'],
                      'client_secret': self.tokens['client_secret'],
                      'redirect_uri': self.tokens['redirect_uri']}
        self.db_o.rewrite("tokens.json",self.tokens)

    def GET(self, txid=None):
        retVal_s = "EMPTY"
        return retVal_s

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        input_json = cherrypy.request.json
        #print(input_json)
        querystring = {
            "name": "anonymous DOGE hodler",
            "message": html.escape(input_json["comment"],True),
            "identifier":"anonymous@dogechain.info",
            "amount": input_json["amount"],
            "currency": "DOGE",
            }
        if not self.auth_tokens:
            loaded = self.load_token()
            if not loaded:
                raise cherrypy.HTTPError(500,"Not logged into Streamlabs")
        topmsg = "An awesome DOGE hodler donated " + str(querystring["amount"]) + " Dogecoins!"
        bottommsg = querystring["message"]
        alert_d = {"type": "donation",
                   "message": topmsg}
        if bottommsg:
            alert_d["usermessage"] = bottommsg
        oauth_session = OAuth2Session(self.tokens["client_id"], token=self.auth_tokens, auto_refresh_kwargs=self.extra,
                                      auto_refresh_url = "https://streamlabs.com/api/v1.0/token", token_updater=self.save_token)
        res = oauth_session.post("https://streamlabs.com/api/v1.0/alerts", params=alert_d)
        #print(alert_d)
        #print(res.text)
# EOF