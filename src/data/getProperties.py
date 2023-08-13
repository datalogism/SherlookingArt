#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 15:01:19 2023

@author: cringwal
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 09:43:16 2023

@author: cringwal
"""

from qwikidata.sparql import return_sparql_query_results
from SPARQLWrapper import SPARQLWrapper, JSON
import json 
import time

def getResult( sparql):  
        """ Get the result from the sparql query
        args: 
            sparql: sparql query
            return the result of the query or False if the query is empty"""     
        try:
            results = return_sparql_query_results(sparql)
            results = results['results']['bindings']
            
            #time.sleep(1.0)
            if len(results) != 0:

                return results
            else:
                return False
        except:
            return False



def get_sparql_properties(QID):
    dataset_query = "SELECT * WHERE {?item wdt:P31*/wdt:P279* wd:"+QID+"; rdfs:label ?itemLabel . ?item ?property ?proplabel. FILTER(LANG(?itemLabel) = 'en') . FILTER(LANG(?proplabel) = 'en') . }"
    return dataset_query
def get_sparql_propertiest2(QID):
    dataset_query = "SELECT * WHERE {?item wdt:P31*/wdt:P279* wd:"+QID+". ?item ?property ?o. ?o  rdfs:label ?o_l . FILTER(LANG(?o_l) = 'en') .}"  
    return dataset_query

repo="/user/cringwal/home/Downloads/"

map_file=repo+'pictures.json'
with open(map_file, encoding="utf8") as user_file:
      pictures = json.load(user_file)


nb=len(pictures.keys())
# print("=============== BEGIN")
# print(" At the begining we have ",nb)
# dict_prop={}
# dict_QID_prop={}
# for QID in pictures.keys():
#     print(QID)
#     query = get_sparql_properties(QID)
#     results = getResult(query)
#     if(results):
#         dict_QID_prop[QID]=[]
#         for result in results:
            
#             prop = result["property"]["value"]
#             if( prop not in dict_prop.keys()):
#                 dict_prop[prop] = 0
#             dict_prop[prop] += 1
#             dict_QID_prop[QID].append(result)            
# print("=============== END")
# #print(" At the end we have ",len(dict_QID_pict.keys()))

# with open(repo+"properties_string.json", 'w') as json_file:
#     json.dump(dict_QID_prop, json_file)
    

nb=len(pictures.keys())
print("=============== BEGIN")
print(" At the begining we have ",nb)
dict_prop={}
dict_QID_prop={}
for QID in pictures.keys():
    print(QID)
    query = get_sparql_propertiest2(QID)
    results = getResult(query)
    if(results):
        dict_QID_prop[QID]=[]
        for result in results:
            
            prop = result["property"]["value"]
            if( prop not in dict_prop.keys()):
                dict_prop[prop] = 0
            dict_prop[prop] += 1
            dict_QID_prop[QID].append(result)            
print("=============== END")
#print(" At the end we have ",len(dict_QID_pict.keys()))

with open(repo+"properties_object.json", 'w') as json_file:
    json.dump(dict_QID_prop, json_file)