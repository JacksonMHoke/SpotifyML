from os import replace
import pandas as pd
import numpy as np
import heapq

''' 
TODO: Algorithm does not work currently because there are features that have near complete uniformitivity.
      Create a way to find a good set of features to base the model off of(unsupervised clustering evaluation model)
'''

def normalize(input, max):
    '''
    normalize: Adds weights to the data so that the columns portray similar values

    Parameters:
        - playlistData - Dataframe of all the playlist data from playlist.csv
    '''
    return input/max

def calcDistance(playlistData, trackID1, trackID2, features):
    '''
    calcDistance: Returns the distance between two songs based on a list of features

    Parameters:
        - playlistData - Dataframe of all the playlist data from playlist.csv
        - trackID1 - Track ID of the first track
        - trackID2 - Track ID of the second track
        - features - list of features to compare distance on
    '''
    row1=playlistData.loc[playlistData['Track']==trackID1]
    row2=playlistData.loc[playlistData['Track']==trackID2] #TODO: MUST MAKE IT SO row2.at[0, feature] accesses the correct index
    dist=0
    for feature in features:
        dist+=(row1.iloc[0][feature]-row2.iloc[0][feature])**2
    dist**=.5
    return dist

def evaluate(playlistData, songData, features, numNeighbors, trackIDS=pd.DataFrame()):
    '''
    evaluate: Returns a score of similarity between the song passed in and the rest of the playlist

    Parameters:
        - playlistData - Dataframe of all playlist data from playlist.csv
        - songData - data of the song being evaluated
        - features - list of features to evaluate on
        - numNeighbors - number of points to average distance from
        - trackIDS - (optional)dictionary of trackids<string, bool> to exclude from playlistData

    Return Value:
        Returns average distance of numNeighbors closest playlist songs according to features passed in
    '''
    neighbors=[] #All values will be negative in this to imitate a maxheap
    for track in playlistData.itertuples():
        #track[1] is the row for trackid
        if track[1] not in trackIDS.itertuples():
            dist=calcDistance(playlistData, track[1], songData[1], features)
            if len(neighbors)<numNeighbors:
                heapq.heappush(neighbors, -1*dist)
            elif heapq.nsmallest(1, neighbors)[0] < -1*dist:
                heapq.heappop(neighbors)
                heapq.heappush(neighbors, -1*dist)
    print("Returning from evaluate: ", sum(neighbors[0:len(neighbors)])*-1/numNeighbors)
    return sum(neighbors[0:len(neighbors)])*-1/numNeighbors

def validate(playlistData, features, sampleSize=2, iterations=2, numNeighbors=3):
    '''
    validate: Returns a score based on the features and playlistData passed in

    Parameters:
        - playlistData - Dataframe of all playlist data from playlist.csv
        - features - list of the features to evaluate on
        - sampleSize - number of rows to exclude and calculate for each evaluation
        - iterations - number of samples to test
        - numNeighbors - number of neighbors to calc average distance with
    '''
    sumScore=0
    for i in range(iterations):
        print("iteration: ", i)
        score=0
        excludeRows=playlistData.sample(n=sampleSize, replace=True)
        for row in excludeRows.itertuples():
            score+=evaluate(playlistData=playlistData, songData=row, features=features, numNeighbors=numNeighbors, trackIDS=excludeRows)
            print("After updating row score now is: ", score)
        sumScore+=score/sampleSize
    print("Returning from validate: ", sumScore/iterations)
    return sumScore/iterations

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

    #normalizing all data so that numbers are ~0-1.5ish
    for (columnName, columnData) in playlistData.iteritems():
        if columnName != 'Genres' and columnName != 'Track':
            playlistData[columnName]=playlistData[columnName].astype(float)
            max=sum(columnData.nlargest(50))/50
            playlistData[columnName]=playlistData[columnName].apply(normalize, args=(max, ))
            print("MEAN OF ", columnName, ": " ,playlistData[columnName].mean())
    print(playlistData)
    
    features = list(playlistData.columns.values[2:])
    features.remove("Genres")
    #variables for feature search
    minScore=10**25
    currScore=10**25
    currFeatures=[]
    minFeature=''

    #choose the single feature that will minimize score
    #repeat until no features can decrease minScore
    while minScore>=currScore:
        currScore=minScore

        #finding the feature that decreases score the most
        for col in features:
            print("Testing column: ", col)
            currFeatures.append(col)
            score=validate(playlistData, currFeatures)
            print("Score calculated for tha column is: ", score)
            if currScore>score:
                print("New best score found for column: ", col)
                currScore=score
                minFeature=col
            currFeatures.remove(col)
        #if a feature was found, continue the process, otherwise terminate
        if minScore>currScore:
            minScore=currScore
            currFeatures.append(minFeature)
            features.remove(minFeature)
            print("new features found: ", currFeatures)
        else:
            print("No better option found")
            break
            
    return currFeatures