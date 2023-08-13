#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 17:23:45 2023

@author: cringwal
"""
import json 

from qwikidata.sparql import return_sparql_query_results
from SPARQLWrapper import SPARQLWrapper, JSON

repo="/user/cringwal/home/Downloads/"
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
def get_results(query):
    """ Get the result from the sparql query"""

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery(query)  # the previous query as a literal string

    return sparql.query().convert()

def get_query(Qid):
    """ Get the query to get the abstract of an item"""

    query = """SELECT ?s ?abstract  where {
    ?s dbo:abstract ?abstract.
    ?s owl:sameAs <http://www.wikidata.org/entity/"""+Qid+""">.
    FILTER (lang(?abstract) = 'en')
    }
    LIMIT 1
    """
    return query

def get_Abstract(Qid):
    """ Get the abstract of an item
    args: 
        Qid: the id of the item
        return the abstract of the item or False if the query is empty
        """  
    #Qid="http://www.wikidata.org/entity/Q19844547"
    #Qid=item['item info']['item_id']

    query = get_query(Qid)

    query = query.replace("\n","").strip()
    e = get_results(query)

    print(query)

    abs_ = ""

    for res in e["results"]["bindings"]:
        if res["abstract"]["value"] != "":
            abs_ = res["abstract"]["value"]

    return abs_


repo="/user/cringwal/home/Downloads/"

           
map_file=repo+'properties_object.json'
with open(map_file, encoding="utf8") as user_file:
      prop_obj = json.load(user_file)

map_file=repo+"properties_string.json"
with open(map_file, encoding="utf8") as user_file:
      prop_strings = json.load(user_file)
      
map_file=repo+"pictures.json"
with open(map_file, encoding="utf8") as user_file:
      pictures = json.load(user_file)
      


focused_types=["http://www.wikidata.org/entity/Q3305213","http://www.wikidata.org/entity/Q860861"]

list_keep=[]
for k in prop_obj.keys():
    for item in prop_obj[k]:
        if(item["property"]["value"]=="http://www.wikidata.org/prop/direct/P31"):
            if(item["o"]["value"] in focused_types):
                list_keep.append(k)   



############# GET DATA OF PROP
dict_prop_lab={}
dict_prop_data={"str":{},"obj":{}}
for k in prop_obj.keys():
    if k in list_keep:
        for item in prop_obj[k]:
            if(item["property"]["value"] not in dict_prop_lab.keys()):
                
                PID= item["property"]["value"].replace("http://www.wikidata.org/prop/direct/","")
                query = get_prop_label(PID)
                results = getResult(query)
                if(results):
                   label= results[0]["p_l"]["value"]  
                else:
                    label= item["property"]["value"].split("/")[-1]
                
                dict_prop_lab[item["property"]["value"]]=label
                dict_prop_data["obj"][label]={"nb":1,"domain":{item["o_l"]["value"]:1}}
            else:
                label=dict_prop_lab[item["property"]["value"]]
                dict_prop_data["obj"][label]["nb"]+=1
                if(item["o_l"]["value"] in dict_prop_data["obj"][label]["domain"]):
                    dict_prop_data["obj"][label]["domain"][item["o_l"]["value"]]+=1
                else:
                    dict_prop_data["obj"][label]["domain"][item["o_l"]["value"]]=1
            
for k in prop_strings.keys():
    if k in list_keep:
        for item in prop_strings[k]:
            if(item["property"]["value"] not in dict_prop_lab.keys()):
                PID= item["property"]["value"].replace("http://www.wikidata.org/prop/direct/","")
                query = get_prop_label(PID)
                results = getResult(query)
                if(results):
                   label= results[0]["p_l"]["value"]  
                else:
                    label= item["property"]["value"].split("/")[-1]
                
                dict_prop_lab[item["property"]["value"]]=label
                dict_prop_data["str"][label]={"nb":1,"type":"str"}
            else:
                label=dict_prop_lab[item["property"]["value"]]
                dict_prop_data["str"][label]["nb"]+=1
                

############## BUILD PROP DS

dict_data={}


for k in prop_obj.keys():
    if k in list_keep :
        if k not in dict_data.keys():
            print("ABS >",k)
            abs_=get_Abstract(k)
            dict_data[k]={"pic":pictures[k],"wiki_abs":abs_,"props":{}}
        for item in prop_obj[k]:
            label=dict_prop_lab[item["property"]["value"]]
            if(label not in dict_data[k]["props"].keys()):
                dict_data[k]["props"][label]=[item["o_l"]["value"]]
            else:
                dict_data[k]["props"][label].append(item["o_l"]["value"])
                
for k in prop_strings.keys():
    if k in list_keep :
        if k not in dict_data.keys():
            print("ABS >",k)
            abs_=get_Abstract(k)
            dict_data[k]={"pic":pictures[k],"wiki_abs":abs_,"props":{}}
        for item in prop_strings[k]:
            label=dict_prop_lab[item["property"]["value"]]
            if(label not in dict_data[k]["props"].keys()):
                dict_data[k]["props"][label]=[item["proplabel"]["value"]]
            else:
                dict_data[k]["props"][label].append(item["proplabel"]["value"])              


with open(repo+"dict_data.json", 'w') as json_file:
    json.dump(dict_data, json_file)

with open(repo+"dict_prop_data.json", 'w') as json_file:
    json.dump(dict_prop_data, json_file)

ab_nb=0
for k in dict_data.keys():
    if(len(dict_data[k]["wiki_abs"])!=0):
       ab_nb+=1
       