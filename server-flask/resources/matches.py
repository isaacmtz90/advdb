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

    def get(self, id, cypher_type):
        if (cypher_type == 'ALL_LIKES'):
            query = """MATCH (x)-[:LIKES]->(y) RETURN x, y"""
            match = cypher.execute(query)

        elif (cypher_type == 'FREE_USERS'):
            query = """MATCH (x:Person) WHERE NOT (x)-[:LIKES]->(y:Person)
                    RETURN x"""
            match = cypher.execute(query)

        elif (cypher_type == 'USER_LIKES'):
            query = """MATCH (x_id :Person {person_id:{x_id}})-[:LIKES]->(y)
                    RETURN y.name AS name"""
            match = cypher.execute(query, x_id = id)

        elif (cypher_type == 'USER_SUGGESTIONS_DEFAULT'):
            query = """MATCH (x_id :Person {person_id:{x_id}}),
                    (y:Person) WHERE NOT (x)-[:LIKES]->(y)
                    AND y.person_id <> {x_id} RETURN y"""
            match = cypher.execute(query, x_id = id)

        elif (cypher_type == 'USER_DISLIKES'):
            query = """MATCH (x_id :Person {person_id:{x_id}})-[:DISLIKES]->(y)
                    RETURN y.name AS name"""
            match = cypher.execute(query, x_id = id)

        elif (cypher_type == 'USER_SUGGESTIONS'):
            query = """MATCH (x {person_id:{x_id}})-[:WATCHED]->(interests)<-[:WATCHED]-(y)
                    WHERE NOT (x)-[:LIKES]-(y) AND x.interested_in = y.gender
                    RETURN collect(y) AS matches, collect(interests) AS interests,
                    count(movie) AS rank
                    ORDER BY count(movie) DESC"""
            match = cypher.execute(query, x_id = id)

        elif (cypher_type == 'WATCH_SUGGESTIONS'):
            query = """MATCH (x {person_id:{x_id}})-[:WATCHED]->(interests)<-[:WATCHED]-(y),
                    (y)-[:WATCHED]-(y_interests) WHERE NOT (x)-[:LIKES]-(y)
                    RETURN collect(DISTINCT y) AS matches,
                    collect(DISTINCT y_interests) AS viewing_suggestions"""
            match = cypher.execute(query, x_id = id)

        elif (cypher_type == 'TEST'):
            query = """MATCH (x {person_id:{x_id}})-[:WATCHED]->(movie)<-[:WATCHED]-(y)
                    WHERE NOT (x)-[:LIKES]-(y)
                    RETURN y, movie,
                    count(movie) ORDER BY count(movie) DESC"""
            match = cypher.execute(query, x_id = id)

        if not match:
            return ({"error": "No suggestions"})

        # print "One\n"
        # print match[0]
        #
        # print "Two\n"
        # print match[1]

        results = []
        # for record in match:
        #     print record
            # results.append({"name": record.name})
        # print match["name"]
        # print x[0]
        # x = match[1]
        # yo = x.movie
        # print match[0].y["name"]
        # print yo["genre"]
        return results
    # def put(self, id):
        #
    def delete(self, id):
        pass
