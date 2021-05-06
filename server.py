#coding: utf-8
import os
import sys
import cherrypy
from app import donation, oauth, auth_p, database
from threading import Semaphore
import os
file_lock = Semaphore()
global_db = database.DB_cl(file_lock)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

#--------------------------------------
def main():
#--------------------------------------
   # Get current directory
   current_dir=''
   cherrypy.Application.current_dir=''
   try:
      current_dir = os.path.dirname(os.path.abspath(__file__))
   except:
      current_dir = os.path.dirname(os.path.abspath(sys.executable))
   # disable autoreload
   cherrypy.engine.autoreload.unsubscribe()

   cherrypy.Application.current_dir = current_dir
   configFileName_s = os.path.join(current_dir, 'server.conf')  # im aktuellen Verzeichnis
   if os.path.exists(configFileName_s) == False:
      configFileName_s = None
   cherrypy.config.update({'server.socket_port': 42069})

   cherrypy.tree.mount(
      None, '/', configFileName_s
   )

   # 2. Eintrag: Method-Dispatcher für die "Applikation" "app" vereinbaren
   cherrypy.tree.mount(
      donation.Application_cl(global_db),
      '/donation',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )
   cherrypy.tree.mount(
      oauth.oauth(global_db),
      '/oauth/streamlabs',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )
   cherrypy.tree.mount(
      auth_p.auth(global_db),
      '/auth',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )
   cherrypy.config.update({'request.show_tracebacks': True})
   # Start server
   cherrypy.engine.start()
   cherrypy.engine.block()

#--------------------------------------
if __name__ == '__main__':
#--------------------------------------
   main()
# EOF
