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



def get_sparql_image(QID):
    dataset_query = "SELECT DISTINCT ?pic WHERE { ?item wdt:P31*/wdt:P279* wd:"+QID+". ?item wdt:P18 ?pic .  }"
    return dataset_query

repo="/user/cringwal/home/Downloads/"

map_file=repo+'artwork_triples.txt'
with open(map_file, 'r') as file: # Use file to refer to the file object
   raw_txt = file.read()

raw_txt=raw_txt.split("\n")

list_of_entities=[ lines.split("\t")[0] for lines in raw_txt]

dict_QID_pict={}


nb=len(list_of_entities)
print("=============== BEGIN")
print(" At the begining we have ",nb)

for i in range(nb):
    print(i,"/",nb)
    QID=list_of_entities[i]
    if QID not in list(dict_QID_pict.keys()):
        query = get_sparql_image(QID)
        results = getResult(query)
        if(results):
            for result in results:
            
                if "pic" in result.keys():
                    pic = result["pic"]["value"]
                    dict_QID_pict[QID]=pic

print("=============== END")
print(" At the end we have ",len(dict_QID_pict.keys()))

with open(repo+"pictures.json", 'w') as json_file:
    json.dump(dict_QID_pict, json_file)