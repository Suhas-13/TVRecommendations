API_KEY = open("credentials.txt").read()
import requests
from collections import Counter as mset


class Show:
    def __init__(self, show_name = None, show_id = None, properties = None):
        self.show_name = show_name
        self.processed=False
        self.recommendations = None
        self.similar = None
        self.found = False
        self.key_words = None
        if (properties):
            self.properties = properties
            self.found = True
            self.processed=True
            self.show_name = properties["name"]
        elif show_id:
            request = requests.get("https://api.themoviedb.org/3/tv/" + str(show_id) + "?api_key=" + API_KEY + "&language=en-US)")
            data = request.json()
            if request.ok:
                self.found = True
                self.properties = data
                self.processed=True
            else:
                self.processed = False
                self.found = False
        else:
            data = requests.get("https://api.themoviedb.org/3/search/tv?api_key=" + API_KEY + "&language=en-US&page=1&query=" + show_name + "&include_adult=true")
            data = data.json()
            if len(data["results"]) != 0:
                self.found = True
                self.properties = data["results"][0]
                self.processed=True
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

    
