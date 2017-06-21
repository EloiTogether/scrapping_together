# coding: utf-8

'''
Projet test AppEngine
Auteur : Eloi Zalczer
Année : 2017

models.py

'''

from google.appengine.ext import ndb

import webapp2

import config

class dictionary_entry(ndb.Model):
    profile = ndb.StringProperty(indexed=True)
    keywords = ndb.StringProperty(repeated=True, indexed=True)

    @classmethod
    def get_profiles(cls):
        res=cls.query(projection=[cls.profile], distinct=True).fetch()
        return res if res else None

    @classmethod
    def get_by_keyword_and_profile(cls, keyword, profile):
        res=cls.query().filter(cls.profile == profile).fetch()
        associated_keywords=[]
        for item in res:
            if keyword in item.keywords:
                associated_keywords+= [x.encode('utf-8') for x in item.keywords]

        return associated_keywords

class extractor_url(ndb.Model):
    url = ndb.StringProperty(indexed=True)