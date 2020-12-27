from helper import *
from Show import Show
from api import *
from flask import Flask, request
import json
from flask import jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

@app.route('/get-popular-shows')
def popular_shows():
    count = int(request.args.get('count'))
    response = {"response":[]}
    for show in get_popular_shows(count):
        response['response'].append({"name":show.show_name, "id":show.properties["id"], "published_date": show.properties["first_air_date"], "overview": show.properties["overview"], "image_url":"http://image.tmdb.org/t/p/w94_and_h141_bestv2" + str(show.properties["poster_path"])})
    response = (jsonify(response))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/search')
def get_search():
    query = str(request.args.get('query'))
    count = int(request.args.get('count'))
    response = {"response":[]}
    for show in search(query, count):
        response['response'].append({"name":show.show_name, "id":show.properties["id"], "published_date": show.properties["first_air_date"], "overview": show.properties["overview"], "image_url":"http://image.tmdb.org/t/p/w94_and_h141_bestv2" + str(show.properties["poster_path"])})
    response = (jsonify(response))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)