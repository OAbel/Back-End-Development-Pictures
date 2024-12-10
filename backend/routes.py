from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == int(id):
            return jsonify(picture)
    return {"message" : f"Picture id {id} not found"},404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    try:
        # Parse JSON data from the request
        new_picture = request.get_json()
        
        # Validate request data
        if not new_picture or "id" not in new_picture:
            return jsonify({"Message": "Invalid request data"}), 400

        # Check for duplicate picture ID
        for picture in data:
            if picture["id"] == new_picture["id"]:
                return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302

        # Add new picture to the data store
        data.append(new_picture)
        return jsonify({"id": new_picture["id"]}), 201

    except Exception as e:
        # Catch unexpected errors and return a meaningful error response
        return jsonify({"Message": str(e)}), 500




######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    update_picture = request.get_json()

    if not update_picture:
        return jsonify({"message": "invalid input"}), 400

    for picture in data:
        if picture["id"] == id:
            picture.update(update_picture), 200
            return jsonify(picture)

    return jsonify({"message" : "picture not found"}), 404



######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return '', 204

    return jsonify({"message" : "picture not found"}), 404
    
