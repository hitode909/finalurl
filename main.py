from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from handlers import *

def main():
    application = webapp.WSGIApplication(
        [
            ('/api', ApiHandler),
            ],
        debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
        main()

