#!Scripts/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, abort, make_response, request
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from py2neo import Graph, Node, Relationship

import data_types

app = Flask(__name__, static_url_path='')
api = Api(app)

######## DATABASE CONNECTION AND TYPE DEFINITION ########

graph = \
    Graph('http://netflixandchill:Muidp457FqQDqgyJ4LQP@netflixandchill.sb02.stations.graphenedb.com:24789/db/data/'
          )

# graph.schema.create_uniqueness_constraint("User", "person_id")
# graph.schema.create_uniqueness_constraint("Movie", "movie_id")
# graph.schema.create_uniqueness_constraint("TV_Show", "tvshow_id")

print 'connected to graph'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(422)
def already_exists(error):
    return make_response(jsonify({'error': 'Entity already exists'}),
                         422)


class User(Resource):

    def __init__(self):

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('person_id', type=str,
                                   required=True, location='json')
        self.reqparse.add_argument('email', type=str,
                                   required=True, location='json')
        self.reqparse.add_argument('name', type=str, location='json',
                                   required=True)
        self.reqparse.add_argument('gender', type=str, location='json')
        self.reqparse.add_argument('age', type=int, location='json')
        self.reqparse.add_argument('interested_in', type=list,
                                   location='json')
        self.reqparse.add_argument('height', type=int, location='json',
                                   default=160)
        self.reqparse.add_argument('likes')
        super(User, self).__init__()

    def get(self, id):
        user = graph.find_one('Person', property_key='person_id',
                              property_value=id)
        if not user:
            abort(404)
        return user.properties

    def put(self, id):
        bob = Node('Person', name='Bob', person_id=id)
        graph.create(bob)
        pass

    def post(self, id):
        args = self.reqparse.parse_args()
        user = graph.find_one('Person', property_key='person_id',
                              property_value=args['person_id'])
        if user:
            return user.properties
        else:
            newPerson = Node( "Person" , person_id= args['person_id'], email=args['email'],
                        name = args['name'], gender= args['gender'], age=args['age'], interested_in=args['interested_in'],
                         height=args['height'])
            #add the likes: likes= args['likes']
            #validate if all the types and structure is correct:
            #user_object = marshal(new_user, data_types.user_fields)
            #print user_object
            #store.save_unique("Person", "person_id", toInsert.person_id, toInsert)
            #store.save(toInsert)
            graph.create(newPerson)
            return ({'created' :newPerson.properties}, 200)

    def delete(self, id):
        pass


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


class TestAPI(Resource):

    def get(self, id):
        return {'id_is': id}

    def put(self, id):

        pass

    def delete(self, id):
        pass


api.add_resource(User, '/users/<int:id>', endpoint='users')
api.add_resource(Movie, '/movies/<int:id>', endpoint='movies')
api.add_resource(TV_Show, '/tv_shows/<int:id>', endpoint='tv_show')
api.add_resource(TestAPI, '/tests/<int:id>', endpoint='test')
print 'resource url created'

if __name__ == '__main__':
    app.run(debug=True)
