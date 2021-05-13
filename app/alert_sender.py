from threading import Semaphore, Thread, Lock
import time, copy, datetime
from requests_oauthlib import OAuth2Session, TokenUpdated

class alert_sender(object):
    def __init__(self, db):
        self.db_o = db
        self.cred_lock = Lock()
        self.msg_lock = Lock()
        self.message_notify = Semaphore(0)
        self.cred_dict = {}
        self.msg_list = []
        self.load_creds()


    def load_creds(self):
        with self.cred_lock:
            self.tokens = self.db_o.read("tokens.json")
            if "tokens" in self.tokens.keys():
                self.auth_tokens = self.tokens["tokens"]
                self.extra = {'client_id': self.tokens['client_id'],
                              'client_secret': self.tokens['client_secret'],
                              'redirect_uri': self.tokens['redirect_uri']}
            self.msg_per_min = self.tokens.setdefault("requests_per_min",2)
            if self.auth_tokens:
                return True
            else:
                return False

    def save_token(self, new_t, do_lock = False):
        if do_lock:
            self.cred_lock.acquire()
        self.tokens["tokens"] = new_t
        self.auth_tokens = new_t
        self.extra = {'client_id': self.tokens['client_id'],
                      'client_secret': self.tokens['client_secret'],
                      'redirect_uri': self.tokens['redirect_uri']}
        self.db_o.rewrite("tokens.json",self.tokens)
        if do_lock:
            self.cred_lock.release()

    def append_msg(self, msg):
        with self.msg_lock:
            self.msg_list.append(copy.deepcopy(msg))
        self.message_notify.release()


    def run(self):
        while True:
            self.message_notify.acquire()
            self.msg_lock.acquire()
            alert_d = self.msg_list.pop(0)
            self.msg_lock.release()
            with self.cred_lock:
                oauth_session = OAuth2Session(self.tokens["client_id"], token=self.auth_tokens, auto_refresh_kwargs=self.extra,
                                              auto_refresh_url="https://streamlabs.com/api/v1.0/token",
                                              token_updater=self.save_token)
                res = oauth_session.post("https://streamlabs.com/api/v1.0/alerts", params=alert_d)
            print("Sent msg", datetime.datetime.now().isoformat())
            time.sleep(60.0/self.msg_per_min)