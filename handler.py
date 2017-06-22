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

        profiles = models.profile.fetch_profile()

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
                    <input type="checkbox" name="all_keywords">Uniquement les fichiers contenant TOUS les mots-cles<br/>
                    <select name="profile">'''

        for item in profiles:
            page += '<option value="'+item.name+'">'+item.name+"</option>"

        page += '''</select>Profil a utiliser
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
        keywords_list=keywords.encode('utf-8').split(',')
        models.profile.add_dictionary(profile, keywords_list)

        #profiles = models.dictionary_entry.get_profiles()
        #if any(item.profile == profile for item in profiles):

        self.response.headers['Content-Type'] = "text/plain"
        self.response.out.write("L'association a bien ete enregistree")
        #ret=functions.updateDict(keywords_list)


class addEntryDict(webapp2.RequestHandler):

    def get(self):

        keywords = self.request.get('keywords')
        profile = self.request.get('profile')
        new_profile = self.request.get('new_profile')

        profiles = models.profile.fetch_profile()
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
            page += '<option value="'+item.name+'">'+item.name+"</option>"

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
                  URL :
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

class profiles(webapp2.RequestHandler):

    def get(self):

        profile=self.request.get('profile')
        keywords=self.request.get('keywords')

        profiles = models.profile.fetch_profile()

        self.response.headers['Content-Type'] = "text/html"

        page = '''<html>
            <head>
                <meta charset="utf-8">
            </head>
              <body>
                <h1>Creation d'un nouveau profil</h1>
                <form action="/newProfile?{profile}" method="get">
                    <input type="text" name="profile" required>
                    <input type="submit" value="Creer">
                </form>
                <form action="/updateDict?{profile}&{keywords}" method="get">
                    <input type="text" name="keywords">
                    <select name="profile">'''

        for item in profiles:
            page += '<option value="'+item.name+'">'+item.name+"</option>"

        page += '''</select>
                    <input type="submit" value="Ajouter">
                </form>
                <form method="post">
                    <select name="profile_2">'''

        for item in profiles:
            page += '<option value="'+item.name+'">'+item.name+"</option>"

        page += '''</select>
                    <input type="submit" name="action" value="update"/>
                    <input type="submit" name="action" value="delete"/>
                </form>
              </body>
            </html>'''

        self.response.out.write(textwrap.dedent(page).format(profile=urllib.urlencode({"profile": profile}), keywords=urllib.urlencode({"keywords": keywords})))

    def post(self):
        profile=self.request.get('profile_2')
        action=self.request.get('action')
        self.response.headers['Content-Type'] = "text/plain"
        if(action=="update"):
            newurl = '/updateProfile?' + urllib.urlencode({'profile': profile})
            return self.redirect(newurl)
        if(action=="delete"):
            try:
                profile_to_delete = models.profile.get_profile(profile)
                profile_to_delete.key.delete()
                self.response.out.write("Le profil a bien ete supprime")
            except:
                self.response.out.write("Le profil n'a pas pu etre supprime")


class updateProfile(webapp2.RequestHandler):

    def get(self):
        profile=self.request.get('profile')
        self.response.headers['Content-Type'] = "text/html"
        page = '''<html>
            <head>
                <meta charset="utf-8">
            </head>
              <body>
                <h1>Modifier une association de mots-cles</h1>'''
        profile_key = models.profile.get_profile(profile)
        i=1
        for dictionary in profile_key.dictionaries:
            page += '<form method="post">'
            page += '<input type="text" name="keywords" value="' + ','.join(dictionary.keywords) + '"/>'
            page += '<input type="submit" value="Modifier"/>'
            page += '<input type="hidden" name="id" value="'+str(i)+'"/>'
            page += '<input type="hidden" name="profile" value="'+profile+'"/>'
            page += '</form>'
            i += 1

        page += '''</body>
            </html>'''

        self.response.out.write(page)

    def post(self):
        dictionary_id=self.request.get('id')
        profile=self.request.get('profile')
        keywords=self.request.get('keywords')
        keywords_list=keywords.encode('utf-8').split(',')
        self.response.headers['Content-Type'] = "text/plain"
        self.response.out.write(dictionary_id)
        profile_key = models.profile.get_profile(profile)
        profile_key.dictionaries[int(dictionary_id)-1].keywords=keywords_list
        profile_key.put()
        self.response.out.write("Dictionnaire modifie")



class newProfile(webapp2.RequestHandler):
    def get(self):
        profile=self.request.get('profile')
        self.response.headers['Content-Type'] = "text/plain"
        if not models.profile.get_profile(profile):
            new_profile=models.profile(name=profile, dictionaries=[])
            new_profile.put()
            self.response.out.write("Le profil a bien ete ajoute")
        else:
            self.response.out.write("Le profil existe deja et n'a pas pu etre ajoute")

class home(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = "text/html"
        self.response.out.write('''<html>
        <head>
            <meta charset="utf-8">
        </head>
        <body>
            <h1>Accueil de la plateforme de scrapping</h1>
            <a href="/getData">Recherche par mots-clés</a><br/>
            <a href="/addExtractor">Ajouter un extracteur import.io</a><br/>
            <a href="/profiles">Gerer les profils</a><br/>
        </body>
        </html>
        ''')

app=webapp2.WSGIApplication([
    ('/', home),
    ('/HelloWorld', HelloWorld),
    ('/getData', getData),
    ('/results', results),
    ('/addEntryDict', addEntryDict),
    ('/updateDict', updateDict),
    ('/addExtractor', addExtractor),
    ('/profiles', profiles),
    ('/newProfile', newProfile),
    ('/updateProfile', updateProfile)
], debug=True)