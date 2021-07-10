from featuresearch import calcDistance, evaluate
import importlib
import spotipy
import json
import pandas as pd
import numpy as np
import random
import heapq
import string
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

importlib.import_module('featuresearch')

#loading app key's to access spotify data
credentials=open('credentials.json')
keys=json.load(credentials)

#instantiating spotify client object
scope="user-library-read"
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=keys['CLIENT_ID'], client_secret=keys['CLIENT_SECRET']),
    auth_manager=SpotifyOAuth(client_id=keys['CLIENT_ID'], client_secret=keys['CLIENT_SECRET'], redirect_uri="http://localhost:8888/callback", scope=scope))

countryCodes =['AL', 'DZ', 'AD', 'AO', 'AG', 'AR', 'AM', 'AU', 'AT', 'AZ',
            'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ', 'BT', 'BO', 'BA',
            'BW', 'BR', 'BN', 'BG', 'BF', 'BI', 'CV', 'KH', 'CM', 'CA', 'TD',
            'CL', 'CO', 'KM', 'CR', 'CI', 'HR', 'CW', 'CY', 'CZ', 'DK', 'DJ',
            'DM', 'DO', 'EC', 'EG', 'SV', 'GQ', 'EE', 'FJ', 'FI', 'FR', 'GA',
            'GM', 'GE', 'DE', 'GH', 'GR', 'GD', 'GT', 'GN', 'GW', 'GY', 'HT',
            'HN', 'HK', 'HU', 'IS', 'IN', 'ID', 'IE', 'IL', 'IT', 'JM', 'JP',
            'JO', 'KZ', 'KE', 'KI', 'KR', 'KW', 'KG', 'LA', 'LV', 'LB', 'LS',
            'LR', 'LI', 'LT', 'LU', 'MO', 'MK', 'MG', 'MW', 'MY', 'MV', 'ML',
            'MT', 'MH', 'MR', 'MU', 'MX', 'FM', 'MD', 'MC', 'MN', 'ME', 'MA',
            'MZ', 'NA', 'NR', 'NP', 'NL', 'NZ', 'NI', 'NE', 'NG', 'NO', 'OM', 'PK',
            'PW', 'PS', 'PA', 'PG', 'PY', 'PE', 'PH', 'PL', 'PT', 'QA', 'RO', 'RU',
            'RW', 'KN', 'LC', 'VC', 'WS', 'SM', 'ST', 'SA', 'SN', 'RS', 'SC', 'SL',
            'SG', 'SK', 'SI', 'SB', 'ZA', 'ES', 'LK', 'SR', 'SZ', 'SE', 'CH', 'SY',
            'TW', 'TZ', 'TH', 'TL', 'TG', 'TO', 'TT', 'TN', 'TR', 'TV', 'UG', 'UA',
            'AE', 'GB', 'US', 'UY', 'UZ', 'VU', 'VN', 'ZM', 'ZW']


def normalize(input, max):
    '''
    normalize: Adds weights to the data so that the columns portray similar values

    Parameters:
        - playlistData - Dataframe of all the playlist data from playlist.csv
    '''
    return input/max

try:
    playlistData = pd.read_csv('playlist.csv')
except:
    print('Playlist.csv does not exist yet, run PlaylistCrawler.py to create it.')
    quit()
maxCols=[]
#normalizing all data so that numbers are ~0-1.5ish
for (columnName, columnData) in playlistData.iteritems():
    if columnName != 'Genres' and columnName != 'Track':
        playlistData[columnName]=playlistData[columnName].astype(float)
        max=sum(columnData.nlargest(50))/50
        maxCols.append(max)
        playlistData[columnName]=playlistData[columnName].apply(normalize, args=(max, ))
        # print("MEAN OF ", columnName, ": " ,playlistData[columnName].mean())
print(playlistData)

features = list(playlistData.columns.values[2:])
features.remove("Genres")
print(features)
bestSongs=[]
for i in range(50):
    randQuery=''
    for j in range(3):
        randQuery=randQuery+random.choice(string.ascii_letters)
    randQuery=randQuery+'%'
    randMarket=random.choice(countryCodes)
    try:
        trackid=spotify.search(q=randQuery, offset=random.randint(0,100), type='track', market=randMarket)
        randIndex=random.randint(0,5)
        audFeatures=spotify.audio_features(tracks=trackid['tracks']['items'][randIndex]['id'])
        #WHERE I LEFT OFF, NEED TO CONVERT AUDIOFEATURES INTO A SONG DATA THING
        playlistData.loc[-1]=[trackid['tracks']['items'][randIndex]['id'], audFeatures[0]['time_signature']/maxCols[0], audFeatures[0]['duration_ms']/maxCols[1], audFeatures[0]['tempo']/maxCols[2], audFeatures[0]['valence']/maxCols[3],
                            audFeatures[0]['liveness']/maxCols[4], audFeatures[0]['instrumentalness']/maxCols[5], audFeatures[0]['acousticness']/maxCols[6], audFeatures[0]['speechiness']/maxCols[7],
                            audFeatures[0]['mode']/maxCols[8], audFeatures[0]['loudness']/maxCols[9], audFeatures[0]['key']/maxCols[10], audFeatures[0]['energy']/maxCols[11], audFeatures[0]['danceability']/maxCols[12], '']
        songData=[0, trackid['tracks']['items'][randIndex]['id']]
        bestSongs.append((trackid['tracks']['items'][randIndex]['name'] + '   /////   ' + trackid['tracks']['items'][randIndex]['artists'][0]['name'], evaluate(playlistData,songData,features,7)))
        print(trackid['tracks']['items'][randIndex]['name'], '\n')
    except:
        countryCodes.remove(randMarket)
bestSongs.sort(key=lambda x:x[1])
print(bestSongs)