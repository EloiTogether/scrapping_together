# coding: utf-8

'''
Projet test AppEngine
Auteur : Eloi Zalczer
Année : 2017

models.py

'''

from google.appengine.ext import ndb
import pickle

import webapp2

import config

class dictionary_entry(ndb.Model):
    keywords = ndb.PickleProperty()

class profile(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    dictionaries = ndb.StructuredProperty(dictionary_entry, repeated=True)

    @classmethod
    def fetch_profile(cls):
        res=cls.query().filter().fetch()
        return res

    @classmethod
    def get_profile(cls, profile):
        res=cls.query().filter(cls.name == profile).get()
        return res

    @classmethod
    def add_dictionary(cls, profile, dictionary):
        res=cls.query().filter(cls.name == profile).get()
        new_dictionary = dictionary_entry(keywords=dictionary)
        res.dictionaries.append(new_dictionary)
        res.put()

class extractor_url(ndb.Model):
    url = ndb.StringProperty(indexed=True)