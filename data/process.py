'''Process the downloaded matches'''

import json
import csv

KEYS = [
    "id",
    "DBNOs",
    "assists",
    "boosts",
    "damageDealt",
    "deathType",
    "headshotKills",
    "heals",
    "killPlace",
    "killPoints",
    "killPointsDelta",
    "killStreaks",
    "kills",
    "lastKillPoints",
    "lastWinPoints",
    "longestKill",
    "mostDamage",
    "name",
    "playerId",
    "rankPoints",
    "revives",
    "rideDistance",
    "roadKills",
    "swimDistance",
    "teamKills",
    "timeSurvived",
    "vehicleDestroys",
    "walkDistance",
    "weaponsAcquired",
    "winPlace",
    "winPoints",
    "winPointsDelta",
    "group_id",
    "stats",
    "tags",
    "mapName",
    "seasonState",
    "createdAt",
    "gameMode",
    "titleId",
    "shardId",
    "isCustomMatch",
    "duration",
]

def import_matches(filename):
    '''Open json file and extract matches'''
    with open(filename) as file:
        return json.load(file)

def matches_to_players(matches):
    '''Extract match data into rows of participants'''
    all_players = {}
    for match in matches:
        # Extract general match information first
        attributes = match["data"]["attributes"]
        players = {}
        for obj in match["included"]:
            if obj["type"] == "participant":
                # Copy stats into player object
                if obj["id"] in players:
                    players[obj["id"]].update(obj["attributes"]["stats"])
                else:
                    players[obj["id"]] = obj["attributes"]["stats"]
                    players[obj["id"]]["group_id"] = -1
                #Add match attributes
                players[obj["id"]].update(attributes)
            elif obj["type"] == "roster":
                # Add a group id to each player in the roster
                for participant in obj["relationships"]["participants"]["data"]:
                    if participant["id"] not in players:
                        players[participant["id"]] = {}
                    players[participant["id"]]["group_id"] = obj["attributes"]["stats"]["teamId"]
        all_players.update(players)
    return all_players

def convert_to_csv(players, filename):
    '''Convert the players into a csv'''
    with open(filename, 'w') as output:
        writer = csv.writer(output)
        #Uncomment to write headers
        #writer.writerow(KEYS)
        for key, value in players.items():
            data = [key] + [value[key] for key in KEYS[1:]]
            writer.writerow(data)

def process_raw_matches():
    '''Process raw matches by asking user for raw data file name'''
    filename = input("Please input the file name for your raw data."\
    "Ex: \"matches-2018-11-18T19:33:05.278801\":\n")
    type(filename)

    matches = import_matches("data/raw/{}".format(filename))
    players = matches_to_players(matches)
    out_filename = "data/processed/{}.csv".format(filename)
    convert_to_csv(players, out_filename)

process_raw_matches()
