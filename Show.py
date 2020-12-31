API_KEY = open("credentials.txt").read()
import requests
from collections import Counter as mset
import json
import time
show_save = json.load(open("show_save.json","r"))

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
            show_save[str(self.show_id)] = self.properties
            show_save[str(self.show_id)]['added_utc'] = time.time()
            json.dump(show_save,open("show_save.json","w+"))
        elif show_id:
            if str(show_id) in show_save:
                #print("Hitting storage")
                self.show_id = show_id
                self.properties = show_save[str(self.show_id)]
                self.show_name = self.properties['original_name']
                print(self.show_name)
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
                    print(self.show_name)
                    self.processed=True
                    show_save[str(show_id)] = self.properties
                    show_save[str(show_id)]['added_utc'] = time.time()
                    json.dump(show_save,open("show_save.json","w+"))
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
                show_save[str(show_id)] = self.properties
                show_save[str(show_id)]['added_utc'] = time.time()
                json.dump(show_save,open("show_save.json","w+"))
            else:
                self.found = False

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

    
