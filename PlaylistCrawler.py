import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import json

credentials=open('credentials.json')
keys=json.load(credentials)

scope="user-library-read"
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=keys['CLIENT_ID'], client_secret=keys['CLIENT_SECRET']),
    auth_manager=SpotifyOAuth(client_id=keys['CLIENT_ID'], client_secret=keys['CLIENT_SECRET'], redirect_uri="http://localhost:8888/callback", scope=scope))

#concatanating offset lists due to limit on number of songs pulled
playlist = spotify.playlist_items(playlist_id="7zea9So7ZqkHJk2sjPSezz?si=89a4b290212a473a", kwargs="target_acousticness")
tracks=playlist['tracks']['items']
while(playlist['tracks']['next']):
    playlist['tracks']=spotify.next(playlist['tracks'])
    tracks.extend(playlist['tracks']['items'])

print(tracks[0]['track']['artists'])
combinedTracks=[]
combinedFeatures=[]
for idx, item in enumerate(tracks):
    if isinstance(item['track']['id'], str) : combinedTracks.append(item['track']['id'])
    if idx%100==0: 
        features=spotify.audio_features(tracks=combinedTracks)
        for feature in features:
            combinedFeatures.append(feature)
        combinedTracks=[]

featuresTrackDict=dict(zip(combinedTracks, combinedFeatures))
print(featuresTrackDict[combinedTracks[-1]])

# print(type(combinedTracks[0]))
# print(features, "LENGTH: ", len(combinedFeatures))

# for idx, item in enumerate(tracks):
#     track=item['track']
#     try:
#         res=spotify.search(track['artists'][0]['name'], limit=1, type='artist')
#     except:
#         print("Local file.")
#     if len(track['artists'])>0 and len(res['artists']['items'])>0 : 
#         print(idx, track['artists'][0]['name'], " - ", res['artists']['items'][0]['genres'])

