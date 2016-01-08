from flask import Flask, jsonify, abort, make_response, request
from flask.ext.restful import  Resource, reqparse, fields, marshal
from database import graphene

graph = graphene.get_database()

class TV_Show(Resource):

    def get(self, id):
        tvshow = graph.find_one('TV_Show', property_key='tvshow_id',
                                property_value=id)
        if len(tvshow) == 0:
            abort(404)
        return tvshow.properties

    def put(self, id):
        pass

    def delete(self, id):
        pass