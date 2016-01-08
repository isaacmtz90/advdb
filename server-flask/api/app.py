#!../Scripts/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, abort, make_response, request
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

from resources import person, movie, tvshow


import data_types
    
app = Flask(__name__, static_url_path='')
api = Api(app)


print 'connected to graph'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(422)
def already_exists(error):
    return make_response(jsonify({'error': 'Entity already exists'}),
                         422)


class TestAPI(Resource):

    def get(self, id):
        return {'id_is': id}

    def put(self, id):

        pass

    def delete(self, id):
        pass


api.add_resource(person.Person, '/users/<string:id>', endpoint='users')
api.add_resource(movie.Movie, '/movies/<string:id>', endpoint='movies')
api.add_resource(tvshow.TV_Show, '/tv_shows/<string:id>', endpoint='tv_show')
api.add_resource(TestAPI, '/tests/<int:id>', endpoint='test')
print 'resource url created'

if __name__ == '__main__':
    app.run(debug=True)
