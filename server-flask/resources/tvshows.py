from flask import Flask, jsonify, abort, make_response, request
from flask.ext.restful import  Resource, reqparse, fields, marshal, marshal_with
from database import graphene, data_types
from py2neo import Node, Relationship

graph = graphene.get_database()

class TV_Shows(Resource):

    def __init__(self):        
        super(TV_Shows, self).__init__()
        
    @marshal_with(data_types.tvshow_list)
    def get(self):
    
        tvshows = graph.find('TV_Show', property_key=None,
                               property_value=None, limit= 200)
        tvshows_object = []
        for tvshow in tvshows:
            tvshows_object.append(tvshow.properties)
        return {'tv_shows' : tvshows_object}

