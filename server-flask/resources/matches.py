from flask import Flask, jsonify, abort, make_response, request
from flask.ext.restful import  Resource, reqparse, fields, marshal, marshal_with
from database import graphene, data_types
from py2neo import Node, Relationship
import json

graph = graphene.get_database()
cypher = graph.cypher

class Matching(Resource):

    def __init__(self):
        #Request parser to get the params in a sexy way
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('entity_type', type=str,
                                   required=True, location='json')
        self.reqparse.add_argument('entity_id', type=str, required=True,
                                   location='json')
        super(Matching, self).__init__()

        # MATCH (a) -[:LIKES]->(m) return a,m
        # MATCH (a:Person {name:"Carlos"}) -[:LIKES]->(m) return m.name
        # MATCH (Taylor:Person), (Erick:Person) WHERE Taylor.name = "Taylor" AND Erick.name = "Erick" CREATE (Taylor)-[:LIKES]->(Erick)
        # MATCH (a:Person) WHERE NOT (a)-[:LIKES]->() RETURN a
        # MATCH (a:Person) WHERE NOT (a)-[:LIKES]->() RETURN DISTINCT a
        # MATCH (a:Person{name:"Erick"}), (m:Person) WHERE NOT (a)-[:LIKES]->(m) AND m.name <> "Erick" RETURN DISTINCT m
        # MATCH (me {name:'Taylor'})-[r:LIKES]->(other)-[r2:LIKES]->(me) RETURN other.name

    def get(self, id, cypher_type = None):
        if (cypher_type == 'FIND_LIKES'):
            query = """MATCH (x_id :Person {person_id:{x_id}})-[:LIKES]->(y)
                    return y.name AS name"""
        elif (cypher_type == 'FIND_DISLIKES'):
            query = """MATCH (x_id :Person {person_id:{x_id}})-[:DISLIKES]->(y)
                    return y.name AS name"""
        elif (cypher_type == 'FIND_SUGGESTIONS'):
            query = """MATCH (x {person_id:{x_id}})-[:WATCHED]->(movie)<-[:WATCHED]-(y)
                    WHERE NOT (x)-[:LIKES]-(y)
                    RETURN collect(y) AS matches, collect(movie) AS movies,
                    count(movie) AS rank
                    ORDER BY count(movie) DESC"""

        query = """MATCH (x {person_id:{x_id}})-[:WATCHED]->(movie)<-[:WATCHED]-(y)
                WHERE NOT (x)-[:LIKES]-(y)
                RETURN y, movie,
                count(movie)
                ORDER BY count(movie) DESC"""
        match = cypher.execute(query, x_id = id)
        # match = cypher.execute("""MATCH (x_id :Person {person_id:{x_id}})
        #                     -[:LIKES]->(y) return y.name AS name""", x_id = id)
        if not match:
            abort(404, message="The requested user doesn't exist")

        results = []
        # print match["name"]
        # for record in match:
            # x =  record
            # results.append({"name": record.name})
        # print x[0]
        x = match[0]
        yo = x.movie
        print yo["genre"]
        return results
    # def put(self, id):
        #
    def delete(self, id):
        pass
