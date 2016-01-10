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
        self.reqparse.add_argument('checked', type=str, required=True,
                                   location='json')
        super(Matching, self).__init__()

    def get(self, id, cypher_type):
        user = graph.find_one('Person', property_key='person_id',
                              property_value=id)

        if (cypher_type == 'ALL_LIKES'):
            query = """MATCH (x)-[:LIKES]->(y) RETURN x, y"""
            match = cypher.execute(query)
            print match

        elif (cypher_type == 'USER_LIKES'):
            query = """MATCH (x_id :Person {person_id:{x_id}})-[:LIKES]->(y)
                    RETURN y.person_id"""
            match = cypher.execute(query, x_id = id)
            print match

        elif (cypher_type == 'USER_SUGGESTIONS_DEFAULT'):
            u = {}
            u['suggestions'] = []
            u['matches'] = []
            u['suggestions'].append(self.get_suggestions_default(id))
            u['matches'].append(self.get_matches(id))
            if u is None:
                return ({"error": "No suggestions"})
            return u

        elif (cypher_type == 'USER_SUGGESTIONS'):
            u = {}
            u['suggestions'] = []
            u['matches'] = []
            u['suggestions'].append(self.get_suggestions(id))
            u['matches'].append(self.get_matches(id))
            if u is None:
                return ({"error": "No suggestions"})
            return u

        elif (cypher_type == 'USER_DISLIKES'):
            u = {}
            u['dislikes'] = []
            u['dislikes'].append(self.get_dislikes(id))
            if u is None:
                return ({"error": "No suggestions"})
            return u
        #
        # elif (cypher_type == 'FREE_USERS'):
        #     query = """MATCH (x:Person) WHERE NOT (x)-[:LIKES]->(y:Person)
        #             RETURN x"""
        #     match = cypher.execute(query)
        #     print match
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

    def put(self, id):
        user = graph.find_one('Person', property_key='person_id',
                              property_value=id)
        print "Hey"
        test = args['checked']
        print test

        if (cypher_type == 'USER_SUGGESTIONS'):
            u = {}
            u['suggestions'] = []
            u['matches'] = []
            u['suggestions'].append(self.get_suggestions(id))
            u['matches'].append(self.get_matches(id))
            if u is None:
                return ({"error": "No suggestions"})
            return u

    def delete(self, id):
        pass

    def get_suggestions (self, person_id):
        query = """MATCH (x:Person {person_id:{x_id}})-[:WATCHED]->(interests)
                <-[:WATCHED]-(y:Person) WHERE NOT (x)-[:LIKES]->(y) AND NOT
                (x)-[:DISLIKES]->(y) AND x.interested_in = y.gender RETURN y"""
        suggestions = cypher.execute(query, x_id = person_id)
        subgraph_person = suggestions.to_subgraph()
        nodelist = []
        for node in subgraph_person.nodes:
            nodelist.append({"person_id":node.properties['person_id'],
                            "name":node.properties['name']})
        return nodelist

    def get_suggestions_default (self, person_id):
        query = """MATCH (x :Person {person_id:{x_id}}),
                (y:Person) WHERE NOT (x)-[:LIKES]->(y)
                AND y.person_id <> {x_id} AND x.interested_in = y.gender
                RETURN y"""
        suggestions = cypher.execute(query, x_id = person_id)
        subgraph_person = suggestions.to_subgraph()
        nodelist = []
        for node in subgraph_person.nodes:
            nodelist.append({"person_id":node.properties['person_id'],
                            "name":node.properties['name']})
        return nodelist

    def get_matches(self, person_id):
        query = """MATCH (x:Person {person_id:{x_id}})-[r:LIKES]->(y)-[r2:LIKES]->(x)
                RETURN y"""
        suggestions = cypher.execute(query, x_id = person_id)
        subgraph_person = suggestions.to_subgraph()
        nodelist = []
        for node in subgraph_person.nodes:
            nodelist.append({"person_id":node.properties['person_id'],
                            "name":node.properties['name']})
        return nodelist

    def get_dislikes(self, person_id):
        query = """MATCH (x:Person {person_id:{x_id}})-[r:DISLIKES]->(y)-[r2:LIKES]->(x)
                RETURN y"""
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
                query = """MATCH (x:Person{person_id: {X}})-[r:LIKES]->(y:Person{person_id: {Y}})-[r2:LIKES]->(x)
                RETURN
                CASE WHEN count(y) > 0
                THEN true
                ELSE false END AS result"""
                check_pairing = cypher.execute(query, X=id, Y=args['entity_id'])
                res = check_pairing[0].result
                return ({'success': 'connection created', 'match':res}, 200)
            return  ({'error': 'one or more nodes doesnt exist'}, 400)
    def delete(self, id):
        pass

class Disconnect(Resource):

    def __init__(self):
        #Request parser to get the params in a sexy way
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('entity_id', type=str, required=True,
                                   location='json')
        super(Disconnect, self).__init__()

    def put(self, id):
        args = self.reqparse.parse_args()
        person_origin = graph.find_one('Person', property_key='person_id',
                              property_value=id)
        if(person_origin):
            person_end = graph.find_one('Person', property_key='person_id',
                        property_value=args['entity_id'])

            if (person_end):
                cypher.execute("MATCH (x:Person{person_id: {X}}),(y:Person {person_id: {Y}}) MATCH (x)-[r1]->(y) DELETE r1", X=id, Y= args['entity_id'])
                person_disliked_user = Relationship(person_origin, "DISLIKES", person_end)
                graph.create_unique(person_disliked_user)
                return  ({'success': 'connection removed'}, 200)
            return  ({'error': 'one or more nodes doesnt exist'}, 400)

    def delete(self, id):
        pass
