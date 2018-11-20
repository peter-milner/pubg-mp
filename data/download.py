"""Downloads sample matches from PUBG API"""

import os
import datetime
import json
import requests
from progress.bar import Bar

API_KEY = os.getenv('PUBG_API_KEY')

HEADER = {
    "Authorization": "Bearer {}".format(API_KEY),
    "Accept": "application/vnd.api+json"
}

def get_sample_matches():
    '''Retrieves sample matches'''

    url = "https://api.pubg.com/shards/pc-na/samples"
    request = requests.get(url, headers=HEADER).json()

    sample_matches = request['data']['relationships']['matches']['data']

    print("{} sample matches were retrieved.".format(len(sample_matches)))

    return sample_matches

def get_match_data(sample_matches):
    '''Retrieves specific match data for the sample_matches provided'''

    print("Retrieiving data about the matches...")

    matches = []

    p_bar = Bar('Downloading', max=len(sample_matches))
    for match in sample_matches:
        url = "https://api.pubg.com/shards/pc-na/matches/{}".format(match['id'])
        request = requests.get(url, headers=HEADER).json()
        matches.append(request)
        p_bar.next()
    p_bar.finish()

    print("Match data for the sample matches was retrieved successfully.")

    file_name = "data/raw/matches-{}".format(datetime.datetime.now().isoformat())

    with open(file_name, 'w') as outfile:
        json.dump(matches, outfile)

    print("Match data saved in \"{}\"".format(file_name))

print("Attempting to grab sample matches...")

get_match_data(get_sample_matches())
