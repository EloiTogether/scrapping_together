# coding: utf-8

'''
Projet test AppEngine
Auteur : Eloi Zalczer
Année : 2017

models.py

'''

from google.appengine.ext import ndb

class dictionary_entry(ndb.Model):
    keywords = ndb.PickleProperty()

class profile(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    dictionaries = ndb.StructuredProperty(dictionary_entry, repeated=True)

    @classmethod
    def fetch_profile(cls):
        #Récupère la liste de tous les profils utilisateur
        res=cls.query().filter().fetch()
        return res

    @classmethod
    def get_profile(cls, profile):
        #Récupère un unique profil correspondant à l'argument donné
        res=cls.query().filter(cls.name == profile).get()
        return res

    @classmethod
    def add_dictionary(cls, profile, dictionary):
        '''Ajoute une liste de mots-clés à la liste de mots-clés associée
        à un profil donné en paramètre'''
        res=cls.query().filter(cls.name == profile).get()
        new_dictionary = dictionary_entry(keywords=dictionary)
        res.dictionaries.append(new_dictionary)
        res.put()

class extractor_url(ndb.Model):
    url = ndb.StringProperty(indexed=True, repeated=True)