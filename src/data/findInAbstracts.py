#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 11:55:56 2023

@author: cringwal
"""
import os
import json 
import itertools
import datefinder
from rdflib import Graph, URIRef, Literal, BNode,Namespace
from rdflib.namespace import RDF
from unidecode import unidecode
import random
import urllib

def find_in_abstract(abstract,value):
   
    if(value.lower() in abstract.lower()):
            return True
    else :
       if(unidecode(value.lower()) in unidecode(abstract.lower())):
           return True 
    return False


focused_prop=["movement","creator"]
focused_ent=['Q4657634',
 'Q3794124',
 'Q1133821',
 'Q920030',
 'Q3642171',
 'Q2734892',
 'Q2900098',
 'Q3948607',
 'Q185255',
 'Q2470123',
 'Q604761',
 'Q28494210',
 'Q644936',
 'Q510799',
 'Q21204853',
 'Q11880391',
 'Q4009226',
 'Q766212',
 'Q6494773',
 'Q3849979',
 'Q3349704',
 'Q2715302',
 'Q3172226',
 'Q1231009',
 'Q3089617',
 'Q3119110',
 'Q2070487',
 'Q29530',
 'Q1988152',
 'Q481454',
 'Q334138',
 'Q2318957',
 'Q4429116',
 'Q683274',
 'Q14127232',
 'Q5659824',
 'Q9372005',
 'Q1167178',
 'Q3842509',
 'Q389198',
 'Q596677',
 'Q5712837',
 'Q493792',
 'Q1103170',
 'Q6163337',
 'Q1913390',
 'Q7973323',
 'Q1213936',
 'Q644106',
 'Q2354033']

map_file="/user/cringwal/home/Desktop/THESE/KC_hackaton/data/dict_data.json"
with open(map_file, encoding="utf8") as user_file:
      data = json.load(user_file)
dict_found_in_abstract={}
nb_movment=0
found_movment=[]
nb_creator=0
found_creator=[]
for k in data.keys():
    if(k in focused_ent):
        print("=======> ",k)
        dict_found_in_abstract[k]={}
        for p in data[k]["props"].keys():
            if p in focused_prop:
                dict_found_in_abstract[k][p]={}
                for item in data[k]["props"][p]:
                    found=find_in_abstract(data[k]["wiki_abs"],item)
                    print("prop >",p," | value :",item," ? ", found)
                    if(found and p=="movement"):
                        nb_movment+=1
                        found_movment.append(item)
                    if(found and p=="creator"):
                        nb_creator+=1
                        found_creator.append(item)
                        

                    
        