from flask import Flask, jsonify, abort, make_response, request
from flask.ext.restful import  Resource, reqparse, fields, marshal, marshal_with
from database import graphene, data_types
from py2neo import Node, Relationship

graph = graphene.get_database()
cypher = graph.cypher

class Connect(Resource):

    def __init__(self):
        #Request parser to get the params in a sexy way
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('entity_type', type=str,
                                   required=True, location='json')
        self.reqparse.add_argument('entity_id', type=str, required=True,
                                   location='json')
        super(Connect, self).__init__()
        
        

    def put(self, id):
        #todo: clean up this messy code. sorrynotsorry
        args = self.reqparse.parse_args()
        person_origin = graph.find_one('Person', property_key='person_id',
                              property_value=id)
        if(person_origin):
            if (args['entity_type'].lower()=='tv_show'):
                tvshow = graph.find_one('TV_Show', property_key='tvshow_id',
                                  property_value=args['entity_id'])
                if (tvshow):
                    person_watched_tvshow= Relationship(person_origin, "WATCHED", tvshow)
                    graph.create_unique(person_watched_tvshow)
                    return  ({'success': 'connection created'}, 200)
                return  ({'error': 'one or more nodes doesnt exist'}, 400)

            elif (args['entity_type'].lower == 'movie'):
                movie = graph.find_one('Movie', property_key='movie_id',
                                  property_value=args['entity_id'])
                if (movie):
                    person_watched_movie= Relationship(person_origin, "WATCHED", movie)
                    graph.create_unique(person_watched_movie)
                    return  ({'success': 'connection created'}, 200)
                return  ({'error': 'one or more nodes doesnt exist'}, 400)
        return({'error': 'person doesnt exist'}, 400)
        
    def delete(self, id):
        pass
    

class Disonnect(Resource):

    def __init__(self):
        #Request parser to get the params in a sexy way
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('entity_type', type=str,
                                   required=True, location='json')
        self.reqparse.add_argument('entity_id', type=str, required=True,
                                   location='json')
        super(Disonnect, self).__init__()
        
        

    def put(self, id):
        #todo: clean up this messy code. sorrynotsorry
        args = self.reqparse.parse_args()
        person_origin = graph.find_one('Person', property_key='person_id',
                              property_value=id)
        if(person_origin):
            if (args['entity_type'].lower()=='tv_show'):
                tvshow = graph.find_one('TV_Show', property_key='tvshow_id',
                                  property_value=args['entity_id'])
                if (tvshow):
                    cypher.execute("MATCH (a:Person{person_id: {A}}),(m:TV_Show {tvshow_id: {B}}) MATCH (a)-[r1]-(m) DELETE r1", A=id, B= args['entity_id'])
                    #person_watched_tvshow= Relationship(person_origin, "WATCHED", tvshow)
                    #person_watched_tvshow.pull()
                    #graph.delete(person_watched_tvshow)
                    return  ({'success': 'connection removed'}, 200)
                return  ({'error': 'one or more nodes doesnt exist'}, 400)

            elif (args['entity_type'].lower == 'movie'):
                movie = graph.find_one('Movie', property_key='movie_id',
                                  property_value=args['entity_id'])
                if (movie):
                    cypher.execute("MATCH (a:Person{person_id: {A}}),(m:Movie {movie_id: {B}}) MATCH (a)-[r1]-(m) DELETE r1", A=id, B= args['entity_id'])
                    return  ({'success': 'connection removed'}, 200)
                return  ({'error': 'one or more nodes doesnt exist'}, 400)
        return({'error': 'person doesnt exist'}, 400)
        
    def delete(self, id):
        pass