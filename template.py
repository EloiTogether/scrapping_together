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
        <table>"""


PAGE_END="""</table>
    </div>
  </body>
</html>
"""

def generateTemplate(ret):

    page=PAGE_BEGIN
    sorted_data = sorted(ret, key=lambda k: k['matches'], reverse=True)
    for item in sorted_data:
        if "www" in item['key']:
            page += '''<tr>
                        <th><a href="'''+item['key']+'">'+item['key']+'''</a></th>
                        <th>'''+item['matches']+'''</th>
                        </tr>'''
        else:
            page += '''<tr>
                        <th>'''+item['key']+'''</th>
                        <th>'''+item['matches']+'''</th>
                        </tr>'''

    page += PAGE_END
    return page