from flask import Flask, jsonify, abort, make_response, request
from flask.ext.restful import  Resource, reqparse, fields, marshal
from database import graphene, data_types
from py2neo import Node, Relationship

graph = graphene.get_database()

class Movie(Resource):

      def __init__(self):
        #Request parser to get the params in a sexy way
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('movie_id', type=str,
                                   required=True, location='json')
        self.reqparse.add_argument('title', type=str, required=True,
                                   location='json')
        self.reqparse.add_argument('year', type=str, location='json',
                                   required=True)
        self.reqparse.add_argument('genre', type=str, location='json')
      
        super(Movie, self).__init__()
        
        
    @marshal_with(data_types.movie_fields)
    def get(self, id):
        
        movie = graph.find_one('Movie', property_key='movie_id',
                               property_value=str(id))
        if not movie:
            abort(404)
        return movie.properties

    def put(self, id):
        pass

    def delete(self, id):
        pass