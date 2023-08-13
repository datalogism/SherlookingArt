#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 17:08:37 2023

@author: cringwal
"""
import json 
repo="/user/cringwal/home/Downloads/"

map_file=repo+'properties_object.json'
with open(map_file, encoding="utf8") as user_file:
      prop_strings = json.load(user_file)
      
prop_to_search="http://www.wikidata.org/prop/direct/P462"

for k in prop_strings:
    for item in prop_strings[k]:
        if(item["property"]["value"]==prop_to_search):
            print(k)
            break