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


#Page d'affichage des resultats de la recherche par mots-cles
class results(webapp2.RequestHandler):

    def get(self):
        #Recuperation des parametres de la requete
        keywords=self.request.get('keywords')
        all_keywords=self.request.get('all_keywords')
        profile=self.request.get('profile')

        #Creation de la liste des mots-cles
        keywords_list=keywords.encode('utf-8').split(',')
        ret=functions.getData(keywords_list, all_keywords, profile)

        #Generation de la page avec le parametre retourne par getData
        page=generateTemplate(ret)
        self.response.write(page)

class getData(webapp2.RequestHandler):

    def get(self):

        keywords=self.request.get('keywords')
        profile=self.request.get('profile')

        #Recuperation de tous les profils
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
                    <select name="profile">
                        <option value="default">Aucun profil</option>'''

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
        self.response.headers['Content-Type'] = "text/plain"
        keywords_list=keywords.encode('utf-8').split(',')
        try:
            models.profile.add_dictionary(profile, keywords_list)
            self.response.out.write("L'association a bien ete enregistree")
        except:
            self.response.out.write("L'association n'a pas pu etre enregistree, merci de reessayer")




class addExtractor(webapp2.RequestHandler):

    def get(self):

        extractors = models.extractor_url.query().get()

        self.response.headers['Content-Type'] = "text/html"
        page = """<html>
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
                    <input type="submit" name="action" value="Ajouter">
                </form>
                <p>ATTENTION : Le formatage de l'extracteur doit etre comme precise dans le README.</p>
                <h2>Liste des extracteurs : </h2>
                """

        i=1
        for url in extractors.url:
            page += '''<form method="post">
                        <p>'''+url+'''"</p>
                        <input type="submit" name="action" value="Supprimer"/>
                        <input type="hidden" name="id" value="'''+str(i)+'''"/>
                    </form>'''
            i += 1

        page += """
              </body>
            </html>"""

        self.response.out.write(page)

    def post(self):
        url=self.request.get("url")
        action = self.request.get("action")
        self.response.headers['Content-Type'] = "text/html"

        if action == "Ajouter":
            try:
                extractors = models.extractor_url.query().get()
                extractors.url.append(url)
                extractors.put()
                self.response.out.write("L'URL a bien ete ajoutee dans la base de donnees")
            except:
                if not extractors:
                    extractors = models.extractor_url(url=[url])
                    extractors.put()
                    self.response.out.write("L'URL a bien ete ajoutee dans la base de donnees")
                else:
                    self.response.out.write("L'URL n'a pas pu etre ajoutee dans la base de donnees. Merci de reessayer")

        elif action == "Supprimer":
            id = self.request.get("id")
            self.response.out.write(id)
            try:
                extractors = models.extractor_url.query().get()
                del extractors.url[int(id)-1]
                extractors.put()
                self.response.out.write("L'URL a bien ete supprimee")
            except:
                self.response.out.write("L'URL n'a pas pu etre supprimee")

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
                    <input type="submit" name="action" value="Modifier"/>
                    <input type="submit" name="action" value="Supprimer"/>
                </form>
              </body>
            </html>'''

        self.response.out.write(textwrap.dedent(page).format(profile=urllib.urlencode({"profile": profile}), keywords=urllib.urlencode({"keywords": keywords})))

    def post(self):
        profile=self.request.get('profile_2')
        action=self.request.get('action')
        self.response.headers['Content-Type'] = "text/plain"
        if(action=="Modifier"):

            #Si on veut modifier la page, redirection vers la page de modification avec le profil
            newurl = '/updateProfile?' + urllib.urlencode({'profile': profile})
            return self.redirect(newurl)
        if(action=="Supprimer"):
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

        #Recuperation de toutes les informations correspondant a un profil
        profile_key = models.profile.get_profile(profile)
        i=1
        for dictionary in profile_key.dictionaries:

            #Utilisation de champs caches pour envoyer les parametres necessaires
            page += '<form method="post">'
            page += '<input type="text" name="keywords" value="' + ','.join(dictionary.keywords) + '"/>'
            page += '<input type="submit" name="action" value="Modifier"/>'
            page += '<input type="submit" name="action" value="Supprimer"/>'
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
        action = self.request.get('action')


        if action == "Modifier":
            keywords_list=keywords.encode('utf-8').split(',')
            self.response.headers['Content-Type'] = "text/plain"
            self.response.out.write(dictionary_id)
            profile_key = models.profile.get_profile(profile)

            #Modification des mots-cles du dictionnaire a l'id donne
            profile_key.dictionaries[int(dictionary_id)-1].keywords=keywords_list
            profile_key.put()
            self.response.out.write("Dictionnaire modifie")

        elif action == "Supprimer":
            profile_key = models.profile.get_profile(profile)
            del profile_key.dictionaries[int(dictionary_id)-1]
            profile_key.put()
            self.response.out.write("Element du dictionnaire supprime")



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
    ('/updateDict', updateDict),
    ('/addExtractor', addExtractor),
    ('/profiles', profiles),
    ('/newProfile', newProfile),
    ('/updateProfile', updateProfile)
], debug=True)