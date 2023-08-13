#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 16:34:45 2023

@author: cringwal
"""
import json 
from qwikidata.sparql import return_sparql_query_results
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd 

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



def get_prop_label(PID):
    dataset_query = "SELECT * WHERE {wd:"+PID+" rdfs:label ?p_l . FILTER(LANG(?p_l) = 'en') .}"
    return dataset_query

repo="/user/cringwal/home/Downloads/"

map_file=repo+'properties_object.json'
with open(map_file, encoding="utf8") as user_file:
      prop_strings = json.load(user_file)

dict_prop={}
for k in prop_strings.keys():
    for item in prop_strings[k]:
        prop = item["property"]["value"]
        if( prop not in dict_prop.keys()):
            dict_prop[prop] = 0
        dict_prop[prop] += 1


dict_prop_name={}
for k in dict_prop.keys():
    PID= k.replace("http://www.wikidata.org/prop/direct/","")
    query = get_prop_label(PID)
    results = getResult(query)
    if(results):
       dict_prop_name[k]= results[0]["p_l"]["value"]

tab=[]
for k in dict_prop.keys():
    temp=[]
    temp.append(k)
    if k in dict_prop_name.keys(): 
        temp.append(dict_prop_name[k])
    else:
        temp.append("")
    temp.append(dict_prop[k])
    tab.append(temp)

        