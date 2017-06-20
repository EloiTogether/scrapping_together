# scrapping_together
Application de scrapping sur vivatech, euratech et lespepitestech
<br/>

## Instructions d'utilisation : 

Le programme télécharge le fichier CSV fourni par import.io après le scrapping. Pour le moment, le scrapping est effectué sur vivatechnology.com, euratechnologies.com et sur les 20 pages les plus récentes de lespepitestech.com (environ les 4 derniers mois).

Les liens de téléchargement CSV sont renseignés dans la variable urls de config.py. Pour ajouter un extracteur :

1. 	Créer l'extracteur sur import.io. Si la page comporte des liens, s'assurer que l'élément contenant le lien s'appelle "Attachment". Si ça ne fonctionne pas, télécharger le fichier CSV et s'assurer manuellement que le champ contenant les liens s'appelle "Attachment_link". Le champ de description doit être nommé "Description".  

2. 	Ajouter l'URL du lien de téléchargement du CSV dans la variable urls de config.py.

Si aucun lien n'est disponible, le programme affichera à la place le premier mot de la description, habituellement le nom de l'entreprise. Si le nom de l'entreprise comporte plusieurs mots, seul le premier sera affiché.

La version la plus récente de l'application est disponible à l'adresse : <https://scrappingtogether-171210.appspot.com/getData>