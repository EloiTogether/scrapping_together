# coding: utf-8

'''
Projet scrapping_together
Auteur : Eloi Zalczer
Année : 2017

template.py

'''

PAGE_BEGIN="""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <style>
      table {
      font-family: arial, sans-serif;
      border-collapse: collapse;
      width: 100%;
      }

      #tables {
      width: 50%;
      margin: auto;
      }

      h1{
      text-align: center;
      }

      td, th {
      border: 1px solid #dddddd;
      text-align: left;
      padding: 8px;
      }

      tr:nth-child(even) {
      background-color: #dddddd;
      }
    </style>
  </head>
  <body>
    <div id="tables">
        <h1>RESULTATS</h1>

        <table>
            <tr>
                <th>URL ou nom de l'entreprise</th>
                <th>Nombre de matches</th>
                <th>Mots-cles associes presents</th>
            </tr>"""


PAGE_END="""</table>
    </div>
  </body>
</html>
"""

def generateTemplate(ret):

    page = PAGE_BEGIN
    sorted_data = sort_keywords(ret)
    for item in sorted_data:
        matches_string=""
        for subitem in item['matches']:
            matches_string += subitem +" : "+str(item['matches'][subitem])+", "

        if item['key'][0] == '!':
            page += '''<tr>
                        <th><a href="'''+item['key'][1:]+'">'+item['key'][1:]+'''</a></th>
                        <th>'''
        else:
            page += '''<tr>
                        <th>'''+item['key']+'''</th>
                        <th>'''
        if item['matches']!="":
                page += matches_string[:-2]+'''</th>
                     <th>'''
        else:
                page += matches_string+'''</th>
                        <th>'''
        if item['additional_keywords']!="":
            page += item['additional_keywords'][:-2]+'''</th>
                        </tr>'''
        else:
            page += item['additional_keywords']+'''</th>
                        </tr>'''

    page += PAGE_END
    return page


def sort_keywords(ret):
    s = sorted(ret, key=lambda k: sum(k['matches'].values()), reverse=True)
    return sorted(s, key=lambda k: sum(x>0 for x in (k['matches']).values()), reverse=True)