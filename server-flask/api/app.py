#!../Scripts/python
# -*- coding: utf-8 -*-

#Code to find modules in the parent path
import os,sys,inspect
#print(sys.path)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)


from flask import Flask, jsonify, abort, make_response, request
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

from resources import person, movie, tvshow, likes, matches, movies, tvshows


from database import data_types

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


api.add_resource(person.Person, '/user/<string:id>', endpoint='user')
api.add_resource(movie.Movie, '/movie/<string:id>', endpoint='movie')
api.add_resource(movies.Movies, '/movies', endpoint='movies')
api.add_resource(tvshow.TV_Show, '/tv_show/<string:id>', endpoint='tv_show')
api.add_resource(tvshows.TV_Shows, '/tv_shows', endpoint='tv_shows')
api.add_resource(likes.Connect, '/add_like/<string:id>', endpoint='likes')
api.add_resource(TestAPI, '/tests/<int:id>', endpoint='test')
api.add_resource(matches.Matching, '/matches/<string:id>', endpoint='matches')
print 'resource url created'


@app.route('/')
def root():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
