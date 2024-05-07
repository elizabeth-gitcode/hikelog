import json
import os
from flask import Flask, Response, jsonify, request
import uuid

app = Flask(__name__)

@app.route("/hikes", methods=['GET'])
def get_hikes():
    hikes = []
    # Iterate over all files in the directory
    for filename in os.listdir("database/hikes"):
        # Check if the current file is a regular file (not a directory)
        filepath = os.path.join("database/hikes", filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                text = file.read()
                hike = json.loads(text)
                hike["id"] = filename
                hikes.append(hike)
                
    return jsonify(hikes)

@app.route('/hikes/<id>', methods=['DELETE'])
def delete_hike(id):
    filepath = os.path.join("database/hikes", id)
    if os.path.isfile(filepath):
        os.remove(filepath)
        return Response("", 200, mimetype='application/json')
    else:
        return Response("", 404, mimetype='application/json')
    
@app.route('/hikes', methods=['POST'])
def post_hike():
    new_hike = request.json
    name = new_hike.get("name")
    elevationGain = new_hike.get("elevationGain")
    distance = new_hike.get("distance")
    rating = new_hike.get("rating")
    
    hike = {"name": name, "elevationGain": elevationGain, "distance": distance, "rating": rating }

    hike_json = json.dumps(hike)

    filepath = os.path.join("database/hikes", str(uuid.uuid4()))
    with open(filepath, 'w') as file:
        file.write(hike_json)
    
    return Response(hike_json, 200, mimetype='application/json')
    

