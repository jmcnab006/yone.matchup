#!/usr/bin/python

import json

def validateJSON(jsonData):
    try:
        json.load(jsonData)
    except ValueError as err:
        return False
    return True 

f = open("./matchup.json")
d = json.load(f)
    
print d

