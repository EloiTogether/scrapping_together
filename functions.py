# coding: utf-8

'''
Projet scrapping_together
Auteur : Eloi Zalczer
Année : 2017

functions.py

'''

import urllib2
import csv
from config import urls, dictionary

def getData(keywords_list, all_keywords):
    responses=[]
    for url in urls:
        try:
            responses.append(urllib2.urlopen(url))
        except:
            pass
    more_keywords=[]
    for keyword in keywords_list:
        more_keywords=more_keywords+[item for item in dictionary if keyword in item]
    if(all_keywords==""):
        return processData_one_keyword(responses, keywords_list, more_keywords)

    else:
        return processData_all_keywords(responses, keywords_list, more_keywords)

def processData_one_keyword(responses, keywords_list, more_keywords):
    ret=[]
    for response in responses:
        data=csv.DictReader(response)
        for row in data:
            nb_matches=0
            keywords_matchs=""
            for keyword in keywords_list:
                nb_matches += row['Description'].count(keyword)
                keywords_matchs += keyword+" : "+str(row['Description'].count(keyword))+", "

            if nb_matches>0:
                additional_keywords=""
                for item in more_keywords:
                    for keyword in item:
                        if keyword in row['Description'] and keyword not in keywords_list:
                            additional_keywords += keyword+", "
                try:
                    if row['Attachment_link']!="":
                        ret.append({'key': row['Attachment_link'].decode('utf-8'),'matches': str(keywords_matchs), 'additional_keywords': additional_keywords})
                except:
                    ret.append({'key': (row['Description'].split('\n', 1)[0]).decode('utf-8'), 'matches': str(keywords_matchs), 'additional_keywords': additional_keywords})

    return ret

def processData_all_keywords(responses, keywords_list, more_keywords):
    ret=[]
    for response in responses:
        data=csv.DictReader(response)
        for row in data:
            match=1
            keywords_matchs=""
            for keyword in keywords_list:
                if keyword not in row['Description']:
                    match=0
                    break
                keywords_matchs += keyword+" : "+str(row['Description'].count(keyword))+", "
            if match:
                additional_keywords=""
                for item in more_keywords:
                    for keyword in item:
                        if keyword in row['Description'] and keyword not in keywords_list:
                            additional_keywords += keyword+", "
                try:
                    if(row['Attachment_link']!=""):
                        ret.append({'key': row['Attachment_link'].decode('utf-8'),'matches': str(keywords_matchs), 'additional_keywords': additional_keywords})
                except:
                    ret.append({'key': (row['Description'].split('\n', 1)[0]).decode('utf-8'), 'matches': str(keywords_matchs), 'additional_keywords': additional_keywords})

    return ret
