# SpotifyML
Program that finds music that I would like using my spotify playlist as data.

# How it's done
More specifically, this algorithm first pulls all the audio features data from my playlist and stores it inside a CSV. After that it uses a feature search to weed out excessive features that could decrease accuracy. After narrowing down the features, it then pulls random songs from spotify and then compares the distance of the n closest songs to give them a rating. It then sorts those songs by rating and outputs them as a list from best match to worst match.

# Playlist Crawler
This python program utilizes the Spotipy api to keep track of all the songs in the playlist and their audio features. In order to avoid having to pull excessive data from the spotify servers, I kept track of the songs in the current playlist and updated the file with only the new songs added after the last execution of this program.

This is an example execution of the playlist crawler. What is shown is the ID of the track being updated and the index of the track in the CSV file.

![Alt text](crawler.png?raw=true "Title")

# Feature Search
This part of the project is not completely functional as my idea for the feature search turned out to be faulty. My original plan was to minimize distance from the n closest songs by choosing suitable features in order to create a good set of features for optimal clusters. My plan fell short when the optimal features for that was no features. With a few tweaks to the algorithm such as a backward elimination approach, the feature search could work, but I ran out of time.

Here is an example execution of the search, what is being shown is the process of evaluating each feature and eliminating them accordingly.

![Alt text](search.PNG?raw=true "Title")

# Song Recommender
The song recommender is the final part of this project. This program will read the CSV file with all the data, then choose random spotify songs and rank them using the evaluator in featuresearch.py. Due to spotify not having a random song function, I had to create a pseudo random way of selecting songs. I randomized the market(ex: US, JP, etc) we were searching in first, then randomized 2 characters to put into a search, and finally put a random offset from 1 to 1000 to offset the search by. This ensures that the tracks chosen can be popular or rather unknown.

Here are 2 pictures of the program running, the lower the assigned number to a song the better the match.

![Alt text](recommender1.PNG?raw=true "Title")

![Alt text](recommender2.PNG?raw=true "Title")

# Next steps
Since this project was more of an experiment of the ideas I had from my Introduction to AI class, my knowledge on machine learning currently is severly lacking. In the future I plan to come back to this project and revise the feature search completely to make it functional and more efficient. After that I plan to create a project that accomplishes the same thing but using machine learning APIs to help create a more optimal algorithm.
