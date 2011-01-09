import os
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import memcache, urlfetch

class Helper(webapp.RequestHandler):
    def get_final_url(self, url): # throws exception
        # has cache?
        url_from_cache = memcache.get(url)
        if url_from_cache is not None:
            logging.info("cache hit: " + url)
            return url_from_cache

        # fetch
        logging.info("fetch: " + url)
        response = urlfetch.fetch(url, follow_redirects = False)
        final_url = response.headers['location'] if 'location' in response.headers else url

        memcache.set(url, final_url, 3600)
        return final_url

    def set_allow_header(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'


class ApiHandler(Helper):
    def get(self):
        url = self.request.get('url')
        if not url:
            self.error(400)
            self.response.out.write('url is required.')
            return

        final_url = url
        try:
            final_url = self.get_final_url(url)
        except urlfetch.Error, error: # urlfetch.Error ???
            logging.warn(error.args)

        self.set_allow_header()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(final_url)


    def options(self, owner_name, schema_name, data_key):
        self.set_allow_header()
        self.response.out.write('options')

