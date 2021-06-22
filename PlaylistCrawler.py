import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import json
import pandas as pd
import numpy as np

#loading app key's to access spotify data
credentials=open('credentials.json')
keys=json.load(credentials)

#instantiating spotify client object
scope="user-library-read"
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=keys['CLIENT_ID'], client_secret=keys['CLIENT_SECRET']),
    auth_manager=SpotifyOAuth(client_id=keys['CLIENT_ID'], client_secret=keys['CLIENT_SECRET'], redirect_uri="http://localhost:8888/callback", scope=scope))

#pulling all the tracks into a playlist object
playlist = spotify.playlist_items(playlist_id="7zea9So7ZqkHJk2sjPSezz?si=89a4b290212a473a", kwargs="target_acousticness")
tracks=playlist['tracks']['items']
while(playlist['tracks']['next']): #iterate over all playlist pages
    playlist['tracks']=spotify.next(playlist['tracks'])
    tracks.extend(playlist['tracks']['items'])

#combine track id's and pass it into a function that gives
#audio features of those tracks into a list of track-features
combinedTracks=[]
combinedFeatures=[]
combinedGenres=[]
combinedDanceability=[]
combinedEnergy=[]
combinedKey=[]
combinedLoudness=[]
combinedMode=[]
combinedSpeechiness=[]
combinedAcousticness=[]
combinedInstrumentalness=[]
combinedLiveness=[]
combinedValence=[]
combinedTempo=[]
combinedTime=[]
combinedTimeSig=[]
for item in tracks:
    #makes sure that song is not a local file
    if isinstance(item['track']['id'], str) : 
        feature=spotify.audio_features(tracks=item['track']['id'])
        res=spotify.artist(item['track']['artists'][0]['id'])
        if (feature!=None and res!=None) :
            combinedTracks.append(item['track']['id'])
            combinedGenres.append(res['genres'])
            combinedDanceability.append(feature[0]['danceability'])
            combinedEnergy.append(feature[0]['energy'])
            combinedKey.append(feature[0]['key'])
            combinedLoudness.append(feature[0]['loudness'])
            combinedMode.append(feature[0]['mode'])
            combinedSpeechiness.append(feature[0]['speechiness'])
            combinedAcousticness.append(feature[0]['acousticness'])
            combinedInstrumentalness.append(feature[0]['instrumentalness'])
            combinedLiveness.append(feature[0]['liveness'])
            combinedValence.append(feature[0]['valence'])
            combinedTempo.append(feature[0]['tempo'])
            combinedTime.append(feature[0]['duration_ms'])
            combinedTimeSig.append(feature[0]['time_signature'])

#creating pandas dataframe
df=pd.DataFrame()
df.insert(0, "Track", combinedTracks, True)
df.insert(1, "Genres", combinedGenres, True)
df.insert(1, "Danceability", combinedDanceability, True)
df.insert(1, "Energy", combinedEnergy, True)
df.insert(1, "Key", combinedKey, True)
df.insert(1, "Loudness", combinedLoudness, True)
df.insert(1, "Mode", combinedMode, True)
df.insert(1, "Speechiness", combinedSpeechiness, True)
df.insert(1, "Acousticness", combinedAcousticness, True)
df.insert(1, "Instrumentalness", combinedInstrumentalness, True)
df.insert(1, "Liveness", combinedLiveness, True)
df.insert(1, "Valence", combinedValence, True)
df.insert(1, "Tempo", combinedTempo, True)
df.insert(1, "Time", combinedTime, True)
df.insert(1, "Time_Sig", combinedTimeSig, True)

#writing data to csv
df.to_csv('playlist.csv')

# print(type(combinedTracks[0]))
# print(features, "LENGTH: ", len(combinedFeatures))
# combinedGenres=[]
# for idx, item in enumerate(tracks):
#     track=item['track']
#     try:
#         res=spotify.search(track['artists'][0]['name'], limit=1, type='artist')
#     except:
#         print("Local File")
#     if len(track['artists'])>0 and len(res['artists']['items'])>0 : 
#         print(idx, track['artists'][0]['name'], " - ", res['artists']['items'][0]['genres'])

