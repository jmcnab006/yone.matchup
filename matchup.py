#!/usr/bin/python3

import json
import urllib.request
import re
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('name', nargs='?', help="name of the champion")
args = parser.parse_args()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



if args.name:
    champion = args.name.lower()
else:
    parser.print_help()
    sys.exit(2)


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

    print("")
    print('{0:<15} {1:<35}'.format("Matchup:", data['name'] + " - '" + data['title'] + "'"))
    print('{0:<15} {1:<35}'.format("Difficulty:", data['difficulty']))
    print('{0:<15} {1:<35}'.format("Roles:", ",".join(data['roles'])))
    print('{0:<15} {1:<35}'.format("Start:", ",".join(data['start_items'])))
    print('{0:<15} {1:<35}'.format("Runes:", ",".join(data['rune_suggestions'])))
    print('{0:<15} {1:<35}'.format("Items:", ",".join(data['build_items'])))
    print('{0:<15} {1:<35}'.format("Summoners:", ",".join(data['summoner_spells'])))
    print()
    print('{0:<15} {1:<35}'.format("Playstyle:", ''.join((f"{k}: {v}  " for k, v in data['playstyleInfo'].items()))))
    print()
    print('{0:<15} {1:<35}'.format("Strategy:", data['strategy']))
    print("")
   
   # ''.join((f" - {i}\n" for i in user_input_array)
    print('{0:<15}\n{1:<35}'.format("Tips:", ''.join((f"\t- {i}\n" for i in data['tips']))))
    print("")

    print('{0:<15}\n{1:<35}'.format("Abilities:", ""))

    # do our passive
    passive_description = data['passive']['description']
    passive_description = re.sub('<[^<]+?>', ' ', passive_description)
    passive_description = re.sub(r'^(.*?( .*?){20}) ', r'\1\n  ', passive_description)
    passive_description = re.sub(r'^(.*?( .*?){30}) ', r'\1\n  ', passive_description)
    passive_str = bcolors.OKGREEN + bcolors.BOLD + data['passive']['name'] + bcolors.ENDC + " [" + bcolors.OKBLUE + "Passive" + bcolors.ENDC + "]" 

    print('  {:<15}'.format(passive_str))
    print('  {:<15}'.format(passive_description))
    print()

    # lets do our keybound abilities 
    key_binds = ["Q", "W", "E", "R"]
    
    for k in key_binds:
        index = key_binds.index(k)
        ability = data['abilities'][index]
        
        cooldowns = ability['cooldownCoefficients']
        ranges = ability['range']

        # remove last element from cooldowns I dont know what they are for and dont seem to match any wiki's this can be altered later
        del cooldowns[-1]
        del ranges[-1]
        
        # for ultimate delete a few more elements from range and cooldown
        if index == 3:
            del cooldowns[-1]
            del cooldowns[-1]

        range_str = "{0:.0f}".format(ranges[0]) if ranges[0] == ranges[1] and ranges[1] == ranges[2] and ranges[2] == ranges[3] and ranges[3] == ranges[4] else '/'.join((f"{i:.0f}" for i in ability['range']))
        cooldown_str = bcolors.BOLD + '/'.join((f"{i:.0f}" for i in ability['cooldownCoefficients'])) + bcolors.ENDC
        
        head = bcolors.OKGREEN + bcolors.BOLD + ability['name'] + bcolors.ENDC + " [" + bcolors.OKBLUE + k + bcolors.ENDC + "] - Cooldown: (" + cooldown_str + ") " + "Range: " + range_str 

        description = ability['description']
        description = re.sub('<[^<]+?>', '', description)
        description = re.sub(r'^(.*?( .*?){20}) ', r'\1\n  ', description)
        #print( '/'.join((f"{i:.0f}" for i in ability['range'])))
        #print('  {0:<10} {1:<15} - {2:<35}\n'.format("Q", data['abilities'][0]['name'] + " (" + '/'.join((f"{i:.0f}" for i in data['abilities'][0]['cooldownCoefficients'])) + ") " , data['abilities'][0]['description']))
        #print('  {0:<10} {1:<15} - {2:<35}\n'.format(key_binds[index], ability['name'] + " (" + '/'.join((f"{i:.0f}" for i in ability['cooldownCoefficients'])) + ") " , ability['description']))
        print('  {0:<4}'.format(head))
        print('  {0:<4}'.format(description))
        print()
        #print('  {0:<10} {1:<15} - {2:<35}\n'.format("","", description))


    
    #print( '/'.join((f"{i:.0f}" for i in data['abilities'][0]['range'])))
    #print('  {0:<10} {1:<15} - {2:<35}\n'.format("Q", data['abilities'][0]['name'] + " (" + '/'.join((f"{i:.0f}" for i in data['abilities'][0]['cooldownCoefficients'])) + ") " , data['abilities'][0]['description']))
    #print('  {0:<10} {1:<15} - {2:<35}\n'.format("W", data['abilities'][1]['name'] + " (" + '/'.join((f"{i:.0f}" for i in data['abilities'][1]['cooldownCoefficients'])) + ") " , data['abilities'][1]['description']))
    #print('  {0:<10} {1:<15} - {2:<35}\n'.format("E", data['abilities'][2]['name'] + " (" + '/'.join((f"{i:.0f}" for i in data['abilities'][2]['cooldownCoefficients'])) + ") " , data['abilities'][2]['description']))
    #print('  {0:<10} {1:<15} - {2:<35}\n'.format("R", data['abilities'][3]['name'] + " (" + '/'.join((f"{i:.0f}" for i in data['abilities'][3]['cooldownCoefficients'])) + ") " , data['abilities'][3]['description']))


    
    


f = open("./matchup.json")
json_matchup = json.load(f)

# do a partial match else print a no champ found matching string

for key in json_matchup['matchups'].keys():
    if key.startswith(champion.lower()):
        champion = key

if champion in json_matchup['matchups'].keys():
    matchup = json_matchup['matchups'][champion]
else:
    print("No champion found in source '" + champion +"'")
    sys.exit(2)

cid = matchup['id']

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

