API_KEY = open("credentials.txt").read()
import requests
from collections import Counter as mset

MAX_RECOMMENDATIONS = 5
class Show:
    def __init__(self, show_name = None, properties = None):
        self.show_name = show_name
        self.processed=False
        self.recommendations = None
        self.key_words = None
        if (properties):
            self.properties = properties
            self.show_name = properties["name"]
        else:
            data = requests.get("https://api.themoviedb.org/3/search/tv?api_key=" + API_KEY + "&language=en-US&page=1&query=" + show_name + "&include_adult=true")
            data = data.json()
            if len(data["results"]) != 0:
                self.found = True
                self.properties = data["results"][0]
                self.processed=True
            else:
                self.found = False

    def get_recommendations(self):
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
                    if (count >= MAX_RECOMMENDATIONS):
                        break
                return self.recommendations
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
                count = 0
                for result in data["results"]:
                    self.key_words.update({result['name']})
                    if (count >= MAX_RECOMMENDATIONS):
                        break
                return self.key_words
            else:
                return mset()

    
