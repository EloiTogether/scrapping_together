# coding: utf-8

'''
Projet test AppEngine
Auteur : Eloi Zalczer
Année : 2017

handler.py

'''

import webapp2
import jinja2
import functions
import urllib
import textwrap
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class HelloWorld(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello world!')

class results(webapp2.RequestHandler):

    def get(self):
        keywords=self.request.get('keywords')
        keywords_list=keywords.encode('utf-8').split(',')
        ret=functions.getData(keywords_list)
        template=JINJA_ENVIRONMENT.get_template('results.html')
        self.response.write(template.render(values=ret))

class getData(webapp2.RequestHandler):

    def get(self):

        keywords=self.request.get('keywords')

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(textwrap.dedent("""<html>
            <head>
                <meta charset="utf-8">
            </head>
              <body>
                <form action="/results?{keywords}" method="get">
                  Keywords:
                    <input type="text" name="keywords" required>
                    <input type="submit" value="Envoyer">
                </form>
              </body>
            </html>""").format(keywords=urllib.urlencode({"keywords": keywords})))

app=webapp2.WSGIApplication([
    ('/HelloWorld', HelloWorld), ('/getData', getData), ('/results', results)
], debug=True)