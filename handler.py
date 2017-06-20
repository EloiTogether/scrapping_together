# coding: utf-8

'''
Projet scrapping_together
Auteur : Eloi Zalczer
Année : 2017

handler.py

'''

import webapp2
import functions
import urllib
import textwrap
from template import generateTemplate

class HelloWorld(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello world!')

class results(webapp2.RequestHandler):

    def get(self):
        keywords=self.request.get('keywords')
        all_keywords=self.request.get('all_keywords')
        keywords_list=keywords.encode('utf-8').split(',')
        ret=functions.getData(keywords_list, all_keywords)
        page=generateTemplate(ret)
        self.response.write(page)

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
                    <input type="checkbox" name="all_keywords">Uniquement les fichiers contenant TOUS les mots-clés
                </form>
                <p>Tous les mots-cles doivent etre separes par une virgule, sans espace.</p>
              </body>
            </html>""").format(keywords=urllib.urlencode({"keywords": keywords})))


# class updateDict(webapp2.RequestHandler):
#
#     def get(self):
#         self.response.headers['Content-Type'] = "text/html"
#         self.response.out.write(textwrap.dedent("""<html>
#             <head>
#                 <meta charset="utf-8">
#             </head>
#               <body>
#                 <form action="/results?{keywords}" method="get">
#                   Keywords:
#                     <input type="text" name="keywords" required>
#                     <input type="submit" value="Envoyer">
#                     <input type="checkbox" name="all_keywords">Uniquement les fichiers contenant TOUS les mots-clés
#                 </form>
#                 <p>Tous les mots-cles doivent etre separes par une virgule, sans espace.</p>
#               </body>
#             </html>"""))

app=webapp2.WSGIApplication([
    ('/HelloWorld', HelloWorld), ('/getData', getData), ('/results', results)
], debug=True)