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
        self.reqparse.add_argument('entity_id', type=str, required=True,
                                   location='json')
        super(Matching, self).__init__()

    def get(self, id, cypher_type):
        user = graph.find_one('Person', property_key='person_id',
                              property_value=id)

        if (cypher_type == 'ALL_LIKES'):
            query = """MATCH (x)-[:LIKES]->(y) RETURN x, y"""
            match = cypher.execute(query)
            print match

        # elif (cypher_type == 'FREE_USERS'):
        #     query = """MATCH (x:Person) WHERE NOT (x)-[:LIKES]->(y:Person)
        #             RETURN x"""
        #     match = cypher.execute(query)
        #     print match
        #
        # elif (cypher_type == 'USER_LIKES'):
        #     query = """MATCH (x_id :Person {person_id:{x_id}})-[:LIKES]->(y)
        #             RETURN y.person_id"""
        #     match = cypher.execute(query, x_id = id)
        #     print match
        #
        # elif (cypher_type == 'USER_SUGGESTIONS_DEFAULT'):
        #     query = """MATCH (x :Person {person_id:{x_id}}),
        #             (y:Person) WHERE NOT (x)-[:LIKES]->(y)
        #             AND y.person_id <> {x_id} RETURN y"""
        #     match = cypher.execute(query, x_id = id)


        elif (cypher_type == 'USER_SUGGESTIONS'):
            u = {}
            u['suggestions'] = []
            u['matches'] = []
            u['suggestions'].append(self.get_suggestions(id))
            u['matches'].append(self.get_matches(id))
            return u
        #
        # elif (cypher_type == 'USER_DISLIKES'):
        #     query = """MATCH (x_id :Person {person_id:{x_id}})-[:DISLIKES]->(y)
        #             RETURN y.name AS name"""
        #     match = cypher.execute(query, x_id = id)
        #
        #
        # elif (cypher_type == 'WATCH_SUGGESTIONS'):
        #     query = """MATCH (x {person_id:{x_id}})-[:WATCHED]->(interests)<-[:WATCHED]-(y),
        #             (y)-[:WATCHED]-(y_interests) WHERE NOT (x)-[:LIKES]-(y)
        #             RETURN collect(DISTINCT y) AS matches,
        #             collect(DISTINCT y_interests) AS viewing_suggestions"""
        #     match = cypher.execute(query, x_id = id)
        #
        # elif (cypher_type == 'TEST'):
        #     query = """MATCH (x {person_id:{x_id}})-[:WATCHED]->(movie)<-[:WATCHED]-(y)
        #             WHERE NOT (x)-[:LIKES]-(y)
        #             RETURN y, movie,
        #             count(movie) ORDER BY count(movie) DESC"""
        #     match = cypher.execute(query, x_id = id)

        if not match:
            return ({"error": "No suggestions"})

        results = []

        return results

    def put(self, id):
        pass

    def delete(self, id):
        pass

    def get_suggestions (self, person_id):
        query = """MATCH (x:Person {person_id:{x_id}})-[:WATCHED]->(interests)
                <-[:WATCHED]-(y:Person) WHERE NOT (x)-[:LIKES]-(y) AND x.interested_in = y.gender
                RETURN y"""
        suggestions = cypher.execute(query, x_id = person_id)
        subgraph_person = suggestions.to_subgraph()
        nodelist = []
        for node in subgraph_person.nodes:
            nodelist.append({"person_id":node.properties['person_id'],
                            "name":node.properties['name']})
        return nodelist

    def get_matches(self, person_id):
        query = """MATCH (x:Person {person_id:{x_id}})->[r:LIKES]->(y)-
                [r2:LIKES]->(x) RETURN y"""
        suggestions = cypher.execute(query, x_id = person_id)
        subgraph_person = suggestions.to_subgraph()
        nodelist = []
        for node in subgraph_person.nodes:
            nodelist.append({"person_id":node.properties['person_id'],
                            "name":node.properties['name']})
        return nodelist

class Connect(Resource):

    def __init__(self):
        #Request parser to get the params in a sexy way
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('entity_id', type=str, required=True,
                                   location='json')
        super(Connect, self).__init__()

    def put(self, id):
        args = self.reqparse.parse_args()
        person_origin = graph.find_one('Person', property_key='person_id',
                              property_value=id)
        if(person_origin):
            person_end = graph.find_one('Person', property_key='person_id',
                        property_value=args['entity_id'])

            if (person_end):
                person_liked_user = Relationship(person_origin, "LIKES", person_end)
                graph.create_unique(person_liked_user)
                return  ({'success': 'connection created'}, 200)
            return  ({'error': 'one or more nodes doesnt exist'}, 400)
    def delete(self, id):
        pass

class Disconnect(Resource):

    def __init__(self):
        #Request parser to get the params in a sexy way
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('entity_id', type=str, required=True,
                                   location='json')
        super(Disonnect, self).__init__()

    def put(self, id):
        args = self.reqparse.parse_args()
        person_origin = graph.find_one('Person', property_key='person_id',
                              property_value=id)
        if(person_origin):
            person_end = graph.find_one('Person', property_key='person_id',
                        property_value=args['entity_id'])

            if (person_end):
                cypher.execute("MATCH (x:Person{person_id: {X}}),(y:Person {person_id: {Y}}) MATCH (x)-[r1]-(y) DELETE r1", X=id, Y= args['entity_id'])
                return  ({'success': 'connection removed'}, 200)
            return  ({'error': 'one or more nodes doesnt exist'}, 400)

    def delete(self, id):
        pass
