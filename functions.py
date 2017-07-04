# coding: utf-8

'''
Projet scrapping_together
Auteur : Eloi Zalczer
Année : 2017

functions.py

'''

import urllib2
import csv
import models


def getData(keywords_list, all_keywords, profile):
    responses=[]
    res = models.extractor_url.query().get()

    #Recuperation de toutes les donnees de scrapping depuis les URL recuperees
    for url in res.url:
        try:
            responses.append(urllib2.urlopen(url))
        except:
            pass

    more_keywords=[]

    #Pour chaque mot-cle, on cherche dans l'entite du profil si des associations contiennent de mot-cle
    #Si on trouve le mot cle, on ajoute les mots-cles associes dans la liste more_keywords
    if profile != "default":
        profile_key = models.profile.get_profile(profile)
        for keyword in keywords_list:
            for dictionary in profile_key.dictionaries:
                if keyword in dictionary.keywords:
                    more_keywords += [x.encode('utf-8') for x in dictionary.keywords if x != keyword]

    if(all_keywords==""):
        return processData_one_keyword(responses, keywords_list, more_keywords)

    else:
        return processData_all_keywords(responses, keywords_list, more_keywords)

def processData_one_keyword(responses, keywords_list, more_keywords):
    ret=[]
    for response in responses:

        #Lecture de chaque reponse en CSV
        data=csv.DictReader(response)

        #Pour chaque ligne de donnees, on recherche les mots-cles presents et on compte leur nombre d'apparitions
        for row in data:
            nb_matches=0
            keywords_matchs={}
            for keyword in keywords_list:
                nb_matches += row['Description'].count(keyword)
                keywords_matchs[keyword] = row['Description'].count(keyword)


            #Si on a a trouve un mot-cle, on ecrit les mots-cles associes dans une chaine de caracteres additional_keywords
            if nb_matches:
                additional_keywords=""
                for keyword in more_keywords:
                    if keyword in row['Description'] and keyword not in keywords_list:
                        additional_keywords += keyword+", "

                #On ajoute les mots-cles trouves et les mots-cles associes dans la variable de retour
                try:

                    #Si l'extracteur ne fournit pas de lien, le champ Attachment_link n'existe pas. On utilise alors
                    #la premiere ligne de la description comme nom de l'entreprise

                    link="!"+row['Attachment_link'].decode('utf-8')
                    ret.append({'key': link,'matches': keywords_matchs, 'additional_keywords': additional_keywords})
                except:
                    ret.append({'key': (row['Description'].split('\n', 1)[0]).decode('utf-8'), 'matches': keywords_matchs, 'additional_keywords': additional_keywords})

    return ret

def processData_all_keywords(responses, keywords_list, more_keywords):
    ret=[]
    for response in responses:
        data=csv.DictReader(response)

        #Pour chaque ligne de donnees, on recherche les mots-cles presents. Si un des mots-cles est absent, on interrompt la recherche sur la ligne
        for row in data:
            match=1
            keywords_matchs={}
            for keyword in keywords_list:
                if keyword not in row['Description']:
                    match=0
                    break
                keywords_matchs[keyword] = row['Description'].count(keyword)

            #Si on n'a pas interrompu la recherche (=trouve tous les mots-cles) alors on cherche les mots-cles associes
            if match:
                additional_keywords=""
                for keyword in more_keywords:
                    if keyword in row['Description'] and keyword not in keywords_list:
                        additional_keywords += keyword+", "
                try:
                    if(row['Attachment_link']!=""):
                        ret.append({'key': row['Attachment_link'].decode('utf-8'),'matches': keywords_matchs, 'additional_keywords': additional_keywords})
                except:
                    ret.append({'key': (row['Description'].split('\n', 1)[0]).decode('utf-8'), 'matches': keywords_matchs, 'additional_keywords': additional_keywords})

    return ret