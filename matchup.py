#!/usr/bin/python3

import json
import urllib.request
import re
import argparse
import sys
import textwrap

parser = argparse.ArgumentParser()
parser.add_argument('name', nargs='?', help="name of the champion")
parser.add_argument('-l', '--local', action='store_true', help="use local matchup.json file")
parser.add_argument('-D', '--DEBUG', action='store_true', help="use local matchup.json file")
args = parser.parse_args()

class color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    GREY = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'


if (args.DEBUG):
    #for number in range(100):
    #    code = "\033[" + str(number) + "m"
    #    print( code + str(number) + color.ENDC)
    print (color.RED + "RED" + color.ENDC)
    print (color.GREEN + "GREEN" + color.ENDC)
    print (color.YELLOW + "YELLOW" + color.ENDC)
    print (color.BLUE + "BLUE" + color.ENDC)
    print (color.PURPLE + "PURPLE" + color.ENDC)
    print (color.CYAN + "CYAN" + color.ENDC)
    print (color.BOLD + "BOLD" + color.ENDC)
    print (color.UNDERLINE + "UNDERLINE" + color.ENDC)
    print (color.GREY + "GREY" + color.ENDC)
    print (color.ITALIC + "ITALIC" + color.ENDC)

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
    print(color.CYAN + 'Matchup:' + color.ENDC)
    print('  {0:<15} {1:<35}'.format("Matchup:", color.BOLD + color.ITALIC + data['name'] + color.ENDC + " - '" + color.PURPLE + data['title'] + color.ENDC + "'"))

    difficulty = data['difficulty'] 
    if difficulty in range(1, 3):
        print('  {0:<15} {1:<35}'.format("Difficulty:", color.GREEN + str(data['difficulty']) + color.ENDC ))
    elif difficulty in range(4, 5):
        print('  {0:<15} {1:<35}'.format("Difficulty:", color.BLUE + str(data['difficulty']) + color.ENDC ))
    elif difficulty in range(6, 7):
        print('  {0:<15} {1:<35}'.format("Difficulty:", color.YELLOW + str(data['difficulty']) + color.ENDC ))
    else:
        print('  {0:<15} {1:<35}'.format("Difficulty:", color.RED + str(data['difficulty']) + color.ENDC ))
    
    print('  {0:<15} {1:<35}'.format("Roles:", ",".join(data['roles'])))
    print('  {0:<15} {1:<35}'.format("Playstyle:", ''.join((f"{k}: {v}  " for k, v in data['playstyleInfo'].items()))))
    print()
    print(color.CYAN + 'Recommendations:' + color.ENDC)
    print('  {0:<15} {1:<35}'.format("Start:", ",".join(data['start_items'])))
    print('  {0:<15} {1:<35}'.format("Runes:", ",".join(data['rune_suggestions'])))
    print('  {0:<15} {1:<35}'.format("Items:", ",".join(data['build_items'])))
    print('  {0:<15} {1:<35}'.format("Summoners:", ",".join(data['summoner_spells'])))
    print()
    strategy = textwrap.wrap(data['strategy'],100)

    print(color.CYAN + 'Strategy:' + color.ENDC)
    print("  " + "\n  ".join(strategy))
    print()
   
    if data['tips']:
        print('{0:<15}\n{1:<35}'.format("Tips:", ''.join((f"\t- {i}\n" for i in data['tips']))))
        print("")

    print(color.CYAN + 'Abilities:' + color.ENDC)

    # do our passive
    passive_description = data['passive']['description']
    passive_description = re.sub('<[^<]+?>', ' ', passive_description)
    pdesc = textwrap.wrap(passive_description, 100)
    passive_str = color.GREEN + color.BOLD + data['passive']['name'] + color.ENDC + " [" + color.BLUE + "Passive" + color.ENDC + "]" 

    print('  {:<15}'.format(passive_str))
    print("  " + "\n  ".join(pdesc))
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
        cooldown_str = color.BOLD + '/'.join((f"{i:.0f}" for i in ability['cooldownCoefficients'])) + color.ENDC
        range_str = color.BOLD + range_str + color.ENDC
        
        head = color.GREEN + color.BOLD + ability['name'] + color.ENDC + " [" + color.BLUE + color.BOLD + k + color.ENDC + "] - Cooldown: (" + cooldown_str + ") " + "Range: " + range_str 

        description = ability['description']
        description = re.sub('<[^<]+?>', '', description)
        desc = textwrap.wrap(description, 100)
        print('  {0:<4}'.format(head))
        print("  " + "\n  ".join(desc))
        print()
    
    
#f = open("./matchup.json")
#json_matchup = json.load(f)

if args.local: 
    f = open("./matchup.json")
    json_matchup = json.load(f)
else:
    matchup_url = 'https://raw.githubusercontent.com/jmcnab006/yone.matchup/main/matchup.json'
    json_matchup = downloadJSON(matchup_url)

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

