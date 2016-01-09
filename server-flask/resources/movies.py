from flask import Flask, jsonify, abort, make_response, request
from flask.ext.restful import  Resource, reqparse, fields, marshal, marshal_with
from database import graphene, data_types
from py2neo import Node, Relationship

graph = graphene.get_database()

class Movies(Resource):

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
        self.reqparse.add_argument('picture_url', type=str, location='json')
      
        super(Movies, self).__init__()
        
    @marshal_with(data_types.movie_list)
    def get(self):
    
        movies = graph.find('Movie', property_key=None,
                               property_value=None, limit= 200)
        return jsonify(movies)

