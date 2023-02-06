#!/usr/bin/python3

import json
import urllib.request
#import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('name', nargs='?', help="name of the champion")
args = parser.parse_args()

if args.name:
    champion = args.name.lower()



def downloadJSON(url):
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    with urllib.request.urlopen(req) as response:
       html = response.read()

    return json.loads(html) 

def printMatchup(data):
    
    print('{0:<15} {1:<35}'.format("Matchup:", data['name'] + " - '" + data['title'] + "'"))
    print('{0:<15} {1:<35}'.format("Difficulty:", data['difficulty']))
    print('{0:<15} {1:<35}'.format("Roles:", ",".join(data['roles'])))
    print('{0:<15} {1:<35}'.format("Start:", ",".join(data['start_items'])))
    print('{0:<15} {1:<35}'.format("Runes:", ",".join(data['rune_suggestions'])))
    print('{0:<15} {1:<35}'.format("Items:", ",".join(data['build_items'])))
    print()
    print('{0:<15} {1:<35}'.format("Strategy:", data['strategy']))
    print("")
   
   # ''.join((f" - {i}\n" for i in user_input_array)
    print('{0:<15}\n{1:<35}'.format("Tips:", ''.join((f"\t- {i}\n" for i in data['tips']))))
    print("")

    print('{0:<15}\n{1:<35}'.format("Abilities:", ""))
    print('  {0:<10} {1:<15} - {2:<35}\n'.format("Passive", data['passive']['name'], data['passive']['description']))
    #print(data['abilities'][0]['cooldownCoefficients'])
    #print( '/'.join((f"{i:.0f}" for i in data['abilities'][0]['cooldownCoefficients'])))
    print('  {0:<10} {1:<15} - {2:<35}\n'.format("Q", data['abilities'][0]['name'] + " (" + '/'.join((f"{i:.0f}" for i in data['abilities'][0]['cooldownCoefficients'])) + ")", data['abilities'][0]['description']))
    print('  {0:<10} {1:<15} - {2:<35}\n'.format("W", data['abilities'][1]['name'] + " (" + '/'.join((f"{i:.0f}" for i in data['abilities'][1]['cooldownCoefficients'])) + ")", data['abilities'][1]['description']))
    print('  {0:<10} {1:<15} - {2:<35}\n'.format("W", data['abilities'][2]['name'] + " (" + '/'.join((f"{i:.0f}" for i in data['abilities'][2]['cooldownCoefficients'])) + ")", data['abilities'][2]['description']))
    print('  {0:<10} {1:<15} - {2:<35}\n'.format("W", data['abilities'][3]['name'] + " (" + '/'.join((f"{i:.0f}" for i in data['abilities'][3]['cooldownCoefficients'])) + ")", data['abilities'][3]['description']))


    
    



f = open("./matchup.json")
#champion = 'aatrox'
json_matchup = json.load(f)

matchup = json_matchup['matchups'][champion]
cid = matchup['id']
#print( matchup)

# read local matchup file

# combine champion data based on id from communitydragon.org

# update runes and item selections from default
# present both in a ascii layout with tips and abilites of enemies

champion_url = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champions/{}.json'.format(cid)
champion_data = downloadJSON(champion_url)

matchup['passive'] = champion_data['passive']
matchup['passive'] = champion_data['passive']
matchup['abilities'] = champion_data['spells']
matchup['name'] = champion_data['name']
matchup['title'] = champion_data['title']
matchup['roles'] = champion_data['roles']
matchup['playstyleInfo'] = champion_data['playstyleInfo']

#print(data)
#print(data['passive']['name'])
#print(data.passive.get('description'))
#print(json.dumps(matchup, sort_keys=True, indent=4))
printMatchup(matchup)

