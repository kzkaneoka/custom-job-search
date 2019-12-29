from flask import Blueprint, jsonify, request

from project.api.sites import Indeed

search_blueprint = Blueprint("search", __name__)


@search_blueprint.route("/search", methods=["POST"])
def search_jobs():
    post_data = request.get_json()
    response_object = {"status": "fail", "message": "Invalid payload."}
    if not post_data:
        return jsonify(response_object), 400
    try:
        words = post_data["words"]
        location = post_data["location"]
        offset = 0
        indeed = Indeed(words, location, offset)
        jobs = indeed.search()
        if jobs:
            response_object["jobs"] = jobs
            response_object["words"] = post_data["words"]
            response_object["location"] = post_data["location"]
            response_object["offset"] = indeed.offset
            response_object["status"] = "success"
            response_object["message"] = "Successfully searched."
            return jsonify(response_object), 200
        else:
            response_object["message"] = "Sorry. Can't find jobs."
            return response_object, 400
    except KeyError:
        return response_object, 400


@search_blueprint.route("/search/next", methods=["POST"])
def search_jobs_next():
    post_data = request.get_json()
    response_object = {"status": "fail", "message": "Invalid payload."}
    if not post_data:
        return jsonify(response_object), 400
    try:
        words = post_data["words"]
        location = post_data["location"]
        offset = post_data["offset"]
        indeed = Indeed(words, location, offset)
        indeed.increment_offset()
        jobs = indeed.search()
        if jobs:
            response_object["jobs"] = jobs
            response_object["words"] = words
            response_object["location"] = location
            response_object["offset"] = indeed.offset
            response_object["status"] = "success"
            response_object["message"] = "Successfully searched."
            return jsonify(response_object), 200
        else:
            response_object["message"] = "Sorry. Can't find jobs."
            return response_object, 400
    except KeyError:
        return response_object, 400


@search_blueprint.route("/search/prev", methods=["POST"])
def search_jobs_prev():
    post_data = request.get_json()
    response_object = {"status": "fail", "message": "Invalid payload."}
    if not post_data:
        return jsonify(response_object), 400
    try:
        words = post_data["words"]
        location = post_data["location"]
        offset = post_data["offset"]
        indeed = Indeed(words, location, offset)
        indeed.decrement_offset()
        jobs = indeed.search()
        if jobs:
            response_object["jobs"] = jobs
            response_object["words"] = words
            response_object["location"] = location
            response_object["offset"] = indeed.offset
            response_object["status"] = "success"
            response_object["message"] = "Successfully searched."
            return jsonify(response_object), 200
        else:
            response_object["message"] = "Sorry. Can't find jobs."
            return response_object, 400
    except KeyError:
        return response_object, 400
