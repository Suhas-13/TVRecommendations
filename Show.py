API_KEY = str(open("credentials.txt").read()).replace("\n","")
import requests
from collections import Counter as mset
import json
from storage import is_show_id_saved, get_show_object, save_show_object
import time

class Show:
    def __init__(self, show_name = None, show_id = None, properties = None):
        self.show_name = show_name
        self.processed=False
        self.recommendations = None
        self.similar = None
        self.found = False
        self.key_words = None
        if (properties):
            #print("Hitting storage")
            self.properties = properties
            self.show_id = self.properties['id']
            self.found = True
            self.processed=True
            self.show_name = properties["name"]
        elif show_id:
            if is_show_id_saved(str(show_id)):
                #print("Hitting storage")
                self.show_id = show_id
                self.properties = get_show_object(str(show_id))
                self.show_name = self.properties['original_name']
                self.processed = True
                self.found = True
            else:
                #print("Hitting network")
                request = requests.get("https://api.themoviedb.org/3/tv/" + str(show_id) + "?api_key=" + API_KEY + "&language=en-US)")
                data = request.json()
                if request.ok:
                    self.found = True
                    self.show_id = show_id
                    self.properties = data
                    self.show_name = self.properties['original_name']
                    self.processed=True
                else:
                    self.processed = False
                    self.found = False
        else:
            #print("Hitting network")
            data = requests.get("https://api.themoviedb.org/3/search/tv?api_key=" + API_KEY + "&language=en-US&page=1&query=" + show_name + "&include_adult=true")
            data = data.json()
            if len(data["results"]) != 0:
                self.found = True
                self.properties = data["results"][0]
                self.processed=True
                self.show_name = self.properties['original_name']
                self.show_id = self.properties['id']
            else:
                self.found = False
        if (self.found and self.processed):
            save_show_object(self.properties)

    def get_recommendations(self, max_recommendations):
        if (self.recommendations):
            return self.recommendations
        else:
            if self.processed and self.properties["id"]:
                data = requests.get("https://api.themoviedb.org/3/tv/" + str(self.properties["id"]) + "/recommendations?api_key=" + API_KEY + "&language=en-US&page=1")
                data = data.json()
                self.recommendations = []
                count = 0
                for result in data["results"]:
                    self.recommendations.append(Show(properties = result))
                    if (count >= max_recommendations):
                        break
                    count+=1
                return self.recommendations
            else:
                return []
    def get_similar_shows(self, max_similar):
        if (self.similar):
            return self.similar
        else:
            if self.processed and self.properties["id"]:
                data = requests.get("https://api.themoviedb.org/3/tv/" + str(self.properties["id"]) + "/similar?api_key=" + API_KEY + "&language=en-US&page=1")
                data = data.json()
                self.similar = []
                count = 0
                for result in data["results"]:
                    self.similar.append(Show(properties = result))
                    if (count >= max_similar):
                        break
                    count+=1
                return self.similar
            else:
                return []
    def get_keywords(self):
        if (self.key_words):
            return self.key_words
        else:
            if self.processed and self.properties["id"]:
                data = requests.get("https://api.themoviedb.org/3/tv/" + str(self.properties["id"]) + "/keywords?api_key=" + API_KEY + "&language=en-US&page=1")
                data = data.json()
                self.key_words = mset()
                for result in data["results"]:
                    self.key_words.update({result['name']})
                return self.key_words
            else:
                return mset()

    
