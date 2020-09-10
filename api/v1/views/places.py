#!/usr/bin/python3
"""places.py"""

from api.v1.views import app_views
from flask import Flask, abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place


app = Flask(__name__)


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def retrieveallbystate(city_id):
    """retrieveall by state"""
    li = []
    f = storage.get(City, city_id)
    if f:
        j = f.places
        for i in j:
            ok = storage.get(Place, i.id)
            li.append(ok.to_dict())
        return jsonify(li)
    else:
        abort(404)


@app_views.route('places/<place_id>', methods=['GET'], strict_slashes=False)
def retrieveall(place_id):
    """retrieveall"""
    f = storage.get(Place, place_id)
    if f:
        return jsonify(f.to_dict())
    else:
        abort(404)


@app_views.route('places/<place_id>', methods=['DELETE'], strict_slashes=False)
def deletebyid(place_id):
    """deletebyid"""
    f = storage.get(Place, place_id)
    if f:
        storage.delete(f)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def postcitybyid(city_id):
    """postcitybyid"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    f = storage.get(City, city_id)
    if f is None:
        abort(404)
    if "name" not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    else:
        req_data = request.get_json()
        req_data['city_id'] = city_id
        ct = Place(**req_data)
        ct.save()
        return make_response(jsonify(ct.to_dict()), 201)


@app_views.route('places/<place_id>', methods=['PUT'])
def putcity(place_id):
    """update ct"""

    ct = storage.get(Place, place_id)
    if ct is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    req_data = request.get_json()
    ct.name = req_data['name']
    ct.save()
    return jsonify(ct.to_dict())


if __name__ == "__main__":
    pass
