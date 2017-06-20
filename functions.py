# coding: utf-8

'''
Projet scrapping_together
Auteur : Eloi Zalczer
Année : 2017

functions.py

'''

import urllib2
import csv
from config import urls

def getData(keywords_list, all_keywords):
    responses=[]
    for url in urls:
        try:
            responses.append(urllib2.urlopen(url))
        except:
            pass
    if(all_keywords==""):
        return processData_one_keyword(responses, keywords_list)

    else:
        return processData_all_keywords(responses, keywords_list)

def processData_one_keyword(responses, keywords_list):
    ret=[]
    for response in responses:
        data=csv.DictReader(response)
        for row in data:
            keywords_matchs=0
            for keyword in keywords_list:
                keywords_matchs += row['Description'].count(keyword)

            if keywords_matchs>0:
                try:
                    if row['Attachment_link']!="":
                        ret.append({'key': row['Attachment_link'].decode('utf-8'),'matches': str(keywords_matchs)})
                except:
                    ret.append({'key': (row['Description'].split('\n', 1)[0]).decode('utf-8'), 'matches': str(keywords_matchs)})

    return ret

def processData_all_keywords(responses, keywords_list):
    ret=[]
    for response in responses:
        data=csv.DictReader(response)
        for row in data:
            match=1
            keywords_matchs=0
            for keyword in keywords_list:
                if keyword not in row['Description']:
                    match=0
                    break
                keywords_matchs += row['Description'].count(keyword)

            if match:
                try:
                    if(row['Attachment_link']!=""):
                        ret.append({'key': row['Attachment_link'].decode('utf-8'),'matches': str(keywords_matchs)})
                except:
                    ret.append({'key': (row['Description'].split('\n', 1)[0]).decode('utf-8'), 'matches': str(keywords_matchs)})

    return ret
