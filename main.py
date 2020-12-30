from helper import *
from Show import Show
from api import *
from flask import Flask, request
import json
from flask import jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

def get_processed_list(shows):
    output_list = []
    for show in shows:
        if (show.properties["poster_path"] is None):
            image_url = "no-image"
        else:
            image_url = "http://image.tmdb.org/t/p/w130_and_h195_bestv2" + str(show.properties["poster_path"])
        if "first_air_date" not in show.properties:
            first_air_date = "Never Aired"
        else:
            first_air_date = show.properties["first_air_date"]
        if "overview" not in show.properties or len(show.properties["overview"]) == 0:
            overview = "No overview."
        else:
            overview = show.properties["overview"]
        output_list.append({"name":show.show_name, "id":show.properties["id"], "published_date": first_air_date, "overview": overview, "image_url":image_url})
    return output_list

@app.route('/get-popular-shows')
def popular_shows():
    count = int(request.args.get('count'))
    output_list = get_processed_list(get_popular_shows(count))
    response = {"response":output_list}
    response = (jsonify(response))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/search')
def get_search():
    query = str(request.args.get('query'))
    count = int(request.args.get('count'))
    response = {"response":get_processed_list(search(query, count))}
    response = (jsonify(response))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route("/generate_recommendation", methods=["POST"])
def get_recommendation():
    response = {"response":[]}
    req = request.get_json()
    if req.get("show_id_list") and req.get("count"):
        output_list = get_processed_list(generate_recommendations(req.get("show_id_list"), int(req.get("count"))))
    response['response'] = output_list
    response = (jsonify(response))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)