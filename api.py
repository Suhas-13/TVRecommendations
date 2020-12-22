API_KEY = open("credentials.txt").read()
import requests
import numpy as np
from Show import Show
from collections import Counter 
from itertools import chain
from helper import *
import gensim.models.keyedvectors as word2vec
from collections import Counter as mset

from nltk.tokenize import word_tokenize, sent_tokenize


import nltk
genre_list = {10759: 'Action & Adventure', 16: 'Animation', 35: 'Comedy', 80: 'Crime', 99: 'Documentary', 18: 'Drama', 10751: 'Family', 10762: 'Kids', 9648: 'Mystery', 10763: 'News', 10764: 'Reality', 10765: 'Sci-Fi & Fantasy', 10766: 'Soap', 10767: 'Talk', 10768: 'War & Politics', 37: 'Western'}

def get_list_by_attribute(show_list, attribute):
    output_list = []
    for episode in show_list:
        if (episode.found):
            output_list.append(episode.properties[attribute])
    return output_list
def update_genre_list():
    data = requests.get("https://api.themoviedb.org/3/genre/tv/list?api_key=" + API_KEY + "&language=en-US").json()
    genres = data["genres"]
    for i in genre_list:
        genres[i["id"]] = i["name"]
def get_list_of_recommendations(show_list):
    output_list = []
    for show in show_list:
        output_list.append(show.get_recommendations())
    return output_list
def get_list_of_keywords(show_list):
    output_list = []
    for show in show_list:
        output_list.append(show.get_keywords())
    return output_list
def get_highest_popularity():
    data = requests.get("https://api.themoviedb.org/3/tv/popular?api_key=" + API_KEY + "&language=en-US&page=1").json()
    if len(data["results"]) != 0:
        return data["results"][0]["popularity"]
    else:
        return 2000
def get_best_recommendations(recommendation_list, show_list, count):
    recommendation_keywords = get_list_of_keywords(recommendation_list)
    show_keywords = list(chain.from_iterable(get_list_of_keywords(show_list)))
    max_popularity_score = get_highest_popularity()
    show_keyword_set = mset()
    for keyword in show_keywords:
        show_keyword_set.update({keyword})
    recommendation_scores = [0] * len(recommendation_keywords)
    for recommendation in range(len(recommendation_list)):
        keyword_score = min(0.5,(sum((recommendation_keywords[recommendation] & show_keyword_set).values()) / sum(recommendation_keywords[recommendation].values())) / 2)
        rating_score = min(0.25,(recommendation_list[recommendation].properties["vote_average"] / 10)/ 4)
        rating_count_score = min(0.25, recommendation_list[recommendation].properties["vote_count"] / 4)
        popularity_score = min(0.25,((recommendation_list[recommendation].properties["popularity"] / max_popularity_score) / 4))
        recommendation_scores[recommendation] = keyword_score + rating_score + rating_count_score + popularity_score
    return_list = []
    i = 0
    while (i<count):
        index = recommendation_scores.index(max(recommendation_scores))
        return_list.append(index)
        recommendation.pop(index)
    return return_list
    
def process_show_list(show_list):
    shows = []
    show_id_list = []

    for show in show_list:
        new_show = Show(show_name = show)
        shows.append(new_show) 
        show_id_list.append(new_show.properties["id"])
    genres = get_list_by_attribute(shows, "genre_ids")
    genres = list(chain.from_iterable(genres))
    genre_frequency = {}
    for i in genres:
        if i in genre_frequency:
            genre_frequency[i]+=1
        else:
            genre_frequency[i]=1
    recommendation_list =  get_list_of_recommendations(shows) 
    recommendation_list = list(chain.from_iterable(recommendation_list))
    rec_name_list = {}
    rec_names_not_unique = []
    for i in recommendation_list:
        if i.properties["id"] not in show_id_list:
            rec_names_not_unique.append(i.properties["name"])
            rec_name_list[i.properties["name"]] = i
    occurence_count = Counter(rec_names_not_unique) 
    common_list = occurence_count.most_common(7) 
    recommendation_list = []
    for show in common_list:
        recommendation_list.append(Show(show[0]))
    get_best_recommendation(recommendation_list, show_list)
    return (recommendation_list[recommendation_similarity.index(max(recommendation_similarity))].show_name)
        

        

            
        
    
    
    