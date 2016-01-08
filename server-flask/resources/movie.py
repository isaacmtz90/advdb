from flask import Flask, jsonify, abort, make_response, request
from flask.ext.restful import  Resource, reqparse, fields, marshal
from database import graphene

graph = graphene.get_database()

class Movie(Resource):

    def get(self, id):
        movie = graph.find_one('Movie', property_key='movie_id',
                               property_value=id)
        if not movie:
            abort(404)
        return movie.properties

    def put(self, id):
        pass

    def delete(self, id):
        pass