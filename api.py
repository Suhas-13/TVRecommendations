API_KEY = str(open("credentials.txt").read()).replace("\n","")
import requests
import numpy as np
from Show import Show
from collections import Counter 
import time
from itertools import chain
from helper import *
import math
from collections import Counter as mset
import json
from storage import save_keyword_list, get_stored_similar, is_keyword_saved
import nltk

global current_time
current_time = 0
genre_list = {10759: 'Action & Adventure', 16: 'Animation', 35: 'Comedy', 80: 'Crime', 99: 'Documentary', 18: 'Drama', 10751: 'Family', 10762: 'Kids', 9648: 'Mystery', 10763: 'News', 10764: 'Reality', 10765: 'Sci-Fi & Fantasy', 10766: 'Soap', 10767: 'Talk', 10768: 'War & Politics', 37: 'Western'}

def get_list_by_attribute(show_list, attribute):
    output_list = []
    if attribute == "genres":
        for episode in show_list:
            if (episode.found):
                if "genres" in episode.properties:
                    output_list.append(episode.properties["genres"])
                else:
                    output_list.append(episode.properties["genre_ids"])
    else:
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
        output_list.append(show.get_recommendations(4))
    return output_list
def get_list_of_keywords(show_list):
    output_list = []
    for show in show_list:
        output_list.append(show.get_keywords())
    return output_list
def get_similar_keywords(keyword, count):
    keyword_list = []
    i=1
    if (is_keyword_saved(keyword)):
        return get_stored_similar(keyword)
    else:
        while (i<=count):
            data = requests.get("https://api.themoviedb.org/3/search/keyword?api_key=" +API_KEY + "&query=" + keyword + "&page=1").json()
            if (len(data) == 0):
                break
            for word in data['results']:
                if (word['name'] != keyword):
                    keyword_list.append(word['name'])
            i+=1
    save_keyword_list(keyword, keyword_list)
    return keyword_list
def get_highest_popularity():
    data = requests.get("https://api.themoviedb.org/3/tv/popular?api_key=" + API_KEY + "&language=en-US&page=1").json()
    if len(data["results"]) != 0:
        return (data["results"][0]["popularity"]/1.5, data["results"][0]["vote_count"]/1.5)
    else:
        return (1500,3000)
def get_best_recommendations(recommendation_list, show_list, count):
    global current_time
    recommendation_keywords = get_list_of_keywords(recommendation_list)
    show_keywords = list(chain.from_iterable(get_list_of_keywords(show_list)))
    max_popularity_score, max_reviews = get_highest_popularity()
    show_keyword_set = mset()
    #print("Finished stage 2 after " + str(time.time()-current_time))
    original_show_list = show_list
    for keyword in show_keywords:
        show_keyword_set.update({keyword})
        synonym_list = get_similar_keywords(keyword,1)
        for synonym in synonym_list:
            show_keyword_set.update({synonym})
    for keyword_list in recommendation_keywords:
        for keyword in keyword_list:
            keyword_list.update({keyword:len(recommendation_list)})
    #print("Finished stage 3 after " + str(time.time()-current_time))
    recommendation_scores = [0] * len(recommendation_keywords)
    scores={}
    unique_keyword_scores = set()
    keyword_score_list = []
    for recommendation in range(len(recommendation_list)):
        keyword_sum = len(recommendation_keywords[recommendation].values())
        if (keyword_sum == 0):
            keyword_score = 0
        else:
            keyword_score = min(1,(sum((recommendation_keywords[recommendation] & show_keyword_set).values()) / keyword_sum))
        keyword_score_list.append([keyword_score, recommendation])
        rating_score = (min(1,(recommendation_list[recommendation].properties["vote_average"] / 10)))
        rating_count_score = min(1, (recommendation_list[recommendation].properties["vote_count"] / max_reviews))
        popularity_score = min(1,((recommendation_list[recommendation].properties["popularity"] / max_popularity_score)))
        recommendation_scores[recommendation] = (rating_score*0.25) + (rating_count_score*0.125) + (popularity_score*0.125)
        unique_keyword_scores.add(keyword_score)
        scores[recommendation_list[recommendation].show_name] = {"rating_score":rating_score, "rating_count_score":rating_count_score,"popularity_score":popularity_score, "actual_score": recommendation_scores[recommendation]}
    #print("Finished stage 4 after " + str(time.time()-current_time))
    maximum_keywords = len(unique_keyword_scores)
    keyword_score_list = sorted(keyword_score_list)
    current_position = 1
    for pos in range(len(keyword_score_list)):
        if pos != 0:
            if keyword_score_list[pos][0] != keyword_score_list[pos-1][0]:
                current_position+=1
        discretized_score = current_position/maximum_keywords
        recommendation_scores[keyword_score_list[pos][1]]+=(discretized_score*0.5)
        scores[recommendation_list[keyword_score_list[pos][1]].show_name]["keyword_score"] = discretized_score
        scores[recommendation_list[keyword_score_list[pos][1]].show_name]["actual_score"] = recommendation_scores[keyword_score_list[pos][1]]
    return_list = []
    i = 0
    #print("Finished stage 5 after " + str(time.time()-current_time))
    res = {recommendation_list[i].show_name: recommendation_scores[i] for i in range(len(recommendation_scores))} 
    while (i<count and len(recommendation_list) != 0):
        index = recommendation_scores.index(max(recommendation_scores))
        return_list.append(recommendation_list[index])
        recommendation_scores.pop(index)
        recommendation_list.pop(index)
        i+=1
    #print("Finished stage 6 after " + str(time.time()-current_time))
    return return_list
    
def generate_recommendations(input_list, count):
    global current_time
    current_time = time.time()
    shows = set()
    show_id_list = set()
    for show_id in input_list:
        new_show = Show(show_id = show_id)
        shows.add(new_show) 
        show_id_list.add(new_show.properties["id"])
    genre_list = []
    genres = get_list_by_attribute(shows, "genres")
    genres = list(chain.from_iterable(genres))
    genre_list = []
    for genre in genres:
        if isinstance(genre, int):
            genre_list.append(genre)
        else:
            genre_list.append(genre['id'])
    genre_frequency = {}
    for i in genre_list:
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
            rec_names_not_unique.append(i.properties["id"])
            rec_name_list[i.properties["id"]] = i
    occurence_count = Counter(rec_names_not_unique) 
    common_list = occurence_count.most_common(8) 
    recommendation_list = set()
    original_shows = shows.copy()
    rec_ids = set()
    for show in common_list:
        current_show = rec_name_list[show[0]]
        if (current_show.properties['id'] not in show_id_list):
            recommendation_list.add(current_show)
            rec_ids.add(current_show.properties['id'])
    if (len(input_list) < 8):
        for show in original_shows:
            similar_shows = show.get_similar_shows(1)
            for new_show in similar_shows:
                if (new_show.properties["id"] not in rec_ids and new_show.properties["id"] not in show_id_list):
                    shows.add(new_show)
                    show_id_list.add(new_show.properties["id"])
    #print("Finished stage 1 after " + str(time.time()-current_time))
    recommendations = get_best_recommendations(list(recommendation_list), list(shows), count)
    #print("Finished final stage after " + str(time.time()-current_time))
    return recommendations
        

def search(query, count):
    data = requests.get("https://api.themoviedb.org/3/search/tv?api_key="+ API_KEY + "&query=" + query + "&include_adult=true").json()
    #print(data)
    show_list = []
    i = 0
    if "results" in data:
        for show in data['results']:
            show_list.append(Show(properties = show))
            if (i==count-1):
                break
            i+=1
    return show_list

def get_popular_shows(count):
    #print("https://api.themoviedb.org/3/tv/popular?api_key=" + API_KEY + "&language=en-US&page=1")
    data = requests.get("https://api.themoviedb.org/3/tv/popular?api_key=" + API_KEY + "&language=en-US&page=1").json()
    show_list = []
    i = 0
    print(data)
    for show in data['results']:
        show_list.append(Show(properties = show))
        if (i==count-1):
            break
        i+=1
    return show_list
