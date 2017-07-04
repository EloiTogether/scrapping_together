# scrapping_together
Application de scrapping sur vivatech, euratech et lespepitestech
<br/>

## Instructions d'utilisation : 

Le programme télécharge le fichier CSV fourni par import.io après le scrapping. Pour le moment, le scrapping est effectué sur vivatechnology.com, euratechnologies.com et sur les 20 pages les plus récentes de lespepitestech.com (environ les 4 derniers mois).

Les liens de téléchargement CSV sont renseignés dans la variable urls de config.py. Pour ajouter un extracteur :

1. 	Créer l'extracteur sur import.io. Si la page comporte des liens, s'assurer que l'élément contenant le lien s'appelle "Attachment". Si ça ne fonctionne pas, télécharger le fichier CSV et s'assurer manuellement que le champ contenant les liens s'appelle "Attachment_link". Le champ de description doit être nommé "Description".  

2. 	Ajouter l'URL du lien de téléchargement du CSV dans la variable urls de config.py.

Si aucun lien n'est disponible, le programme affichera à la place le premier mot de la description, habituellement le nom de l'entreprise. Si le nom de l'entreprise comporte plusieurs mots, seul le premier sera affiché.

La version la plus récente de l'application est disponible à l'adresse : <https://scrappingtogether-171210.appspot.com>

Les différentes fonctionnalités disponibles sont : 

1. Recherche par mots-clés :  avec un nombre de mots-clés laissé libre à l'utilisateur. Ces mots-clés doivent être séparés par une virgule, sans espace, comme indiqué en-dessous du champ. L'utilisateur peut choisir d'effectuer une recherche en OU ou ET. Par défaut, le choix est Aucun profil.

2. Gestion de profils : Le logiciel propose une fonctionnalité de gestion de profils permettant à chaque utilisateur de personnaliser sa recherche. Ces profils doivent avoir des noms uniques. La page de gestion des profils permet la création, la gestion et la suppression d'un profil. A chaque profil est associée une ou plusieurs listes de mots-clés associé, qui peuvent être ajoutées ou modifiées. Ces listes permettent d'effectuer une sous-recherche sur chacun des mots-clés qu'elles contiennent lorsqu'un de ces mots-clés est utilisé. 

	Par exemple, si un dictionnaire contient les associations "big data,machine learning,deep learning,profilematching" et que l'utilisateur lance une recherche en utilisant (entre autres) le mot-clé "big data", le logiciel indiquera dans les résultats la présence éventuelle d'un autre mot-clé du dictionnaire.

3. Ajout de lien import.io : Cette page permet d'ajouter un extracteur import.io, préalablement configuré, à la liste d'extracteurs du logiciel. Cet extracteur doit être configuré comme précisé plus haut.

##Documentation

1. Recherche par mots-clés. 
La fonction prend comme paramètres la liste des mots-clés renvoyée par le handler, un argument booleen all_keywords indiquant si la recherche est en OU ou ET et le profil à utiliser. On lance une requête sur la base pour récupérer la liste des liens des extracteurs, puis on récupère le profil donné par l'identifiant si ce dernier n'est pas "default", ce qui correspond à l'entrée *Aucun profil*. Pour chaque lien, on appelle la fonction urlopen() et on récupère les données correspondantes dans la variable *responses*. Pour chaque mot-clé, on vérifie ensuite dans les dictionnaires de l'utilisateur si on le trouve. Si c'est le cas, alors on ajoute les mots-clés associés à la liste more_keywords. Enfin, en fonction de all_keywords, on appelle la fonction *processData_one_keyword* ou *processData_all_keywords*.

	*processData_one_keyword* permet de faire la recherche en mode OU. Pour chaque réponse donnée par urlopen(), on parse le CSV en dictionnaire pour récupérer les données. Pour chaque ligne lue, on vérifie la présence de chacun des mots-clés dans le champ **Description**. Les mots-clés trouvés sont ajoutés dans un dictionnaire avec comme valeur le nombre de fois où ils ont été trouvés. Si au moins un des mots-clés a été trouvé, alors on parcourt les mots-clés associés *more_keywords* et on ajoute les éventuels mots-clés associés trouvés à une chaîne de caractères.
	Si l'extracteur contient un champ *Attachment_link*, on envoie le lien en ajoutant le symbole '!' en premier caractère pour signaler au programme qu'il s'agit d'un lien. Sinon, on envoie la première ligne du champ Description.
	La valeur totale de retour est une liste de dictionnaires, contenant un champ "key" correspondant à l'affichage, un champ "keywords" correspondant à un dictionnaire de mots-clés trouvés avec leur nombre d'apparitions et une chaîne de caractères "additional_keywords".

	*processData_all_keywords* fonctionne approximativement de la même façon que *processData_one_keyword*.  On forme le dictionnaire de valeurs, on parcourt les valeurs du champ Description, cette fois avec une condition d'arrêt "match" qui arrête la recherche de mots-clés si on ne trouve pas un des mots-clés. Le reste est le même que dans la fonction précédente.

