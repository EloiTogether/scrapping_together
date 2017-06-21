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
import models

class HelloWorld(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write("Hello World")

class results(webapp2.RequestHandler):

    def get(self):
        keywords=self.request.get('keywords')
        all_keywords=self.request.get('all_keywords')
        profile=self.request.get('profile')
        keywords_list=keywords.encode('utf-8').split(',')
        ret=functions.getData(keywords_list, all_keywords, profile)
        page=generateTemplate(ret)
        self.response.write(page)
        # keywords=models.dictionary_entry.get_by_keyword("entreprises")
        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.out.write(str(keywords[0]))

class getData(webapp2.RequestHandler):

    def get(self):

        keywords=self.request.get('keywords')
        profile=self.request.get('profile')

        profiles = models.dictionary_entry.get_profiles()

        page='''<html>
            <head>
                <meta charset="utf-8">
            </head>
              <body>
              <h1>Recherche par mots-cles dans la liste de startups</h1>
                <form action="/results?{keywords}&{profile}" method="get">
                  Keywords:
                    <input type="text" name="keywords" required>
                    <input type="submit" value="Envoyer">
                    <input type="checkbox" name="all_keywords">Uniquement les fichiers contenant TOUS les mots-cles
                    <select name="profile">'''

        for item in profiles:
            page += '<option value="'+item.profile+'">'+item.profile+"</option>"

        page += '''</select>
                </form>
                <p>Tous les mots-cles doivent etre separes par une virgule, sans espace.</p>
              </body>
            </html>'''

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(textwrap.dedent(page).format(keywords=urllib.urlencode({"keywords": keywords}), profile=urllib.urlencode({"profile": profile})))


class updateDict(webapp2.RequestHandler):

    def get(self):
        keywords=self.request.get('keywords')
        profile=self.request.get('profile')
        new_profile=self.request.get('new_profile')
        keywords_list=keywords.encode('utf-8').split(',')
        if(profile=="default"):
            if new_profile!="":
                new_entry=models.dictionary_entry(keywords=keywords_list, profile=new_profile)
            else:
                return self.response.out.write("Veuillez entrer un nom de profil")
        else:
            new_entry=models.dictionary_entry(keywords=keywords_list, profile=profile)

        #profiles = models.dictionary_entry.get_profiles()
        #if any(item.profile == profile for item in profiles):

        self.response.headers['Content-Type'] = "text/plain"
        try :
            new_entry.put()
            self.response.out.write("L'association a bien ete enregistree")
        except :
            self.response.out.write("L'association n'a pas pu etre enregistree, merci de reessayer")

        #ret=functions.updateDict(keywords_list)


class addEntryDict(webapp2.RequestHandler):

    def get(self):

        keywords = self.request.get('keywords')
        profile = self.request.get('profile')
        new_profile = self.request.get('new_profile')

        profiles = models.dictionary_entry.get_profiles()
        page = '''<html>
            <head>
                <meta charset="utf-8">
            </head>
              <body>
                <h1>Ajout d'entrees dans le dictionnaire de mots associes</h1>
                <form action="/updateDict?{keywords}&{profile}&{new_profile}" method="get">
                  Keywords:
                    <input type="text" name="keywords" required>
                    <input type="submit" value="Envoyer">
                    <select name="profile">
                        <option value="default">Nouveau profil</option>
                        '''
        for item in profiles:
            page += '<option value="'+item.profile+'">'+item.profile+"</option>"

        page += """</select>Selectionner un profil OU creer un nouveau profil :
                    <input type="text" name="new_profile">
                </form>
                <p>Tous les mots-cles doivent etre separes par une virgule, sans espace.</p>
              </body>
            </html>"""
        self.response.headers['Content-Type'] = "text/html"
        self.response.out.write(textwrap.dedent(page).format(keywords=urllib.urlencode({"keywords": keywords}), profile=urllib.urlencode({"profile": profile}), new_profile=urllib.urlencode({"new_profile": new_profile})))


class addExtractor(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = "text/html"
        self.response.out.write("""<html>
            <head>
                <meta charset="utf-8">
                <style>
                    #url{
                        width: 80%;
                    }
                </style>
            </head>
              <body>
                <h1>Ajout d'un extracteur import.io</h1>
                <form method="post">
                  Keywords:
                    <input id="url" type="text" name="url" required>
                    <input type="submit" value="Envoyer">
                </form>
                <p>ATTENTION : Le formatage de l'extracteur doit etre comme precise dans le README.</p>
              </body>
            </html>""")

    def post(self):
        url=self.request.get("url")
        new_url = models.extractor_url(url=url)
        self.response.headers['Content-Type'] = "text/html"
        try:
            new_url.put()
            self.response.out.write("L'URL a bien ete ajoutee dans la base de donnees")
        except:
            self.response.out.write("L'URL n'a pas pu etre ajoutee dans la base de donnees. Merci de reessayer")



app=webapp2.WSGIApplication([
    ('/HelloWorld', HelloWorld),
    ('/getData', getData),
    ('/results', results),
    ('/addEntryDict', addEntryDict),
    ('/updateDict', updateDict),
    ('/addExtractor', addExtractor)
], debug=True)