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
        output_list.append(show.get_recommendations(5))
    return output_list
def get_list_of_keywords(show_list):
    output_list = []
    for show in show_list:
        output_list.append(show.get_keywords())
    return output_list
def get_similar_keywords(keyword, count):
    keyword_list = []
    i=1
    while (i<=count):
        data = requests.get("https://api.themoviedb.org/3/search/keyword?api_key=" +API_KEY + "&query=" + keyword + "&page=1").json()
        if (len(data) == 0):
            break
        for word in data['results']:
            if (word['name'] != keyword):
                keyword_list.append(word['name'])
        i+=1
    return keyword_list
def get_highest_popularity():
    data = requests.get("https://api.themoviedb.org/3/tv/popular?api_key=" + API_KEY + "&language=en-US&page=1").json()
    if len(data["results"]) != 0:
        return (data["results"][0]["popularity"], data["results"][0]["vote_count"])
    else:
        return (2000,4000)
def get_best_recommendations(recommendation_list, show_list, count):
    recommendation_keywords = get_list_of_keywords(recommendation_list)
    show_keywords = list(chain.from_iterable(get_list_of_keywords(show_list)))
    max_popularity_score, max_reviews = get_highest_popularity()
    show_keyword_set = mset()
    original_show_list = show_list
    for keyword in show_keywords:
        show_keyword_set.update({keyword})
        synonym_list = get_similar_keywords(keyword,1)
        for synonym in synonym_list:
            show_keyword_set.update({synonym})
    for keyword_list in recommendation_keywords:
        for keyword in keyword_list:
            keyword_list.update({keyword:len(recommendation_list)})
    recommendation_scores = [0] * len(recommendation_keywords)
    scores={}
    for recommendation in range(len(recommendation_list)):
        keyword_score = min(1,(sum((recommendation_keywords[recommendation] & show_keyword_set).values()) / len(recommendation_keywords[recommendation].values())))
        rating_score = min(1,(recommendation_list[recommendation].properties["vote_average"] / 10))
        rating_count_score = min(1, (recommendation_list[recommendation].properties["vote_count"] / max_reviews))
        popularity_score = min(1,((recommendation_list[recommendation].properties["popularity"] / max_popularity_score)))
        recommendation_scores[recommendation] = (keyword_score * 0.25) + (rating_score*0.5) + (rating_count_score*0.125) + (popularity_score*0.125)
        scores[recommendation_list[recommendation].show_name] = {"keyword_score":keyword_score,"rating_score":rating_score,"rating_count_score":rating_count_score,"popularity_score":popularity_score, "actual_score": recommendation_scores[recommendation]}
    return_list = []
    i = 0
    res = {recommendation_list[i].show_name: recommendation_scores[i] for i in range(len(recommendation_scores))} 
    while (i<count and len(recommendation_list) != 0):
        index = recommendation_scores.index(max(recommendation_scores))
        return_list.append(recommendation_list[index])
        recommendation_scores.pop(index)
        recommendation_list.pop(index)
        i+=1
    return return_list
    
def process_show_list(show_list, count):
    shows = set()
    show_id_list = set()
    for show in show_list:
        new_show = Show(show_name = show)
        shows.add(new_show) 
        show_id_list.add(new_show.properties["id"])
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
    common_list = occurence_count.most_common(10) 
    recommendation_list = set()
    original_shows = shows.copy()
    rec_ids = set()
    for show in common_list:
        current_show = Show(show[0])
        if (current_show.properties['id'] not in show_id_list):
            recommendation_list.add(current_show)
            rec_ids.add(current_show.properties['id'])
    if (len(show_list) < 8):
        for show in original_shows:
            similar_shows = show.get_similar_shows(2)
            for new_show in similar_shows:
                if (new_show.properties["id"] not in rec_ids and new_show.properties["id"] not in show_id_list):
                    shows.add(new_show)
                    show_id_list.add(new_show.properties["id"])
    return get_best_recommendations(list(recommendation_list), list(shows), count)
        

        

            
        
    
    
    