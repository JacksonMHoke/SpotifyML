import pandas as pd
import numpy as np
import sys

def calcDistance(playlistData, trackID1, trackID2, features):
    '''
    calcDistance: Returns the distance between two songs based on a list of features

    Parameters:
        - playlistData - Dataframe of all the playlist data from playlist.csv
        - trackID1 - Track ID of the first track
        - trackID2 - Track ID of the second track
        - features - list of features to compare distance on
    '''
    return 0


def evaluate(playlistData, songData, features, trackIDS={}):
    '''
    evaluate: Returns a score of similarity between the song passed in and the rest of the playlist

    Parameters:
        - playlistData - Dataframe of all playlist data from playlist.csv
        - songData - data of the song being evaluated
        - features - list of features to evaluate on
        - trackIDS - (optional)dictionary of trackids<string, bool> to exclude from playlistData

    Return Value:
        Returns average distance of 5 closest playlist songs according to features passed in
    '''
    return 0

def validate():
    '''
    validate: Returns a score based on the features and playlistData passed in

    Parameters:
        - playlistData - Dataframe of all playlist data from playlist.csv
        - features - list of the features to evaluate on
    '''
    return 0

def featureSearch():
    '''
    featureSearch: Reads playlist data and finds an efficient set of features to use

    Parameters: None

    Return: An efficient list of features for the evaluate function
    '''
    #reading playlist data
    try:
        playlistData = pd.read_csv('playlist.csv')
    except:
        print('Playlist.csv does not exist yet, run PlaylistCrawler.py to create it.')
        quit()
    features = list(playlistData.columns.values)

    #variables for feature search
    minScore=sys.maxint
    currScore=sys.maxint-1
    currFeatures=[]
    minFeature=''

    #choose the single feature that will minimize score
    #repeat until no features can decrease minScore
    while minScore>currScore:
        currScore=minScore

        #finding the feature that decreases score the most
        for col in features:
            currFeatures.append(col)
            score=validate(playlistData, currFeatures)
            if currScore>score:
                currScore=score
                minFeature=col
            currFeatures.remove(col)
        #if a feature was found, continue the process, otherwise terminate
        if minScore>currScore:
            minScore=currScore
            currFeatures.append(minFeature)
            features.remove(minFeature)
        else:
            break

    return currFeatures

    
