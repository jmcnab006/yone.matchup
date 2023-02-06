#!/usr/bin/python 
#

import urllib2, json

url = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champions/1.json"
data = urllib2.urlopen(url).read()
data = json.loads(data)
print data
