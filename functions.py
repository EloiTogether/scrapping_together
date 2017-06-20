# coding: utf-8

'''
Projet scrapping_together
Auteur : Eloi Zalczer
Année : 2017

functions.py

'''

#from google.appengine.ext import ndb

import urllib2
import csv
from config import urls
from collections import OrderedDict

def getData(keywords_list):
    responses=[]
    for url in urls:
        responses.append(urllib2.urlopen(url))

    ret=[]
    for response in responses:
        data=csv.DictReader(response)
        for row in data:
            keywords_matchs=0
            for keyword in keywords_list:
                keywords_matchs += row['Cell Er Block'].count(keyword)

            if keywords_matchs>0:
                try:
                    if(row['Attachment_link']!=""):
                        ret.append({'key': row['Attachment_link'].decode('utf-8'),'matches': str(keywords_matchs)})
                except:
                    ret.append({'key': (row['Cell Er Block'].split('\n', 1)[0]).decode('utf-8'), 'matches': str(keywords_matchs)})

    return ret