from flask import Flask, jsonify, abort, make_response, request
from flask.ext.restful import Resource, reqparse, fields, marshal, marshal_with
from database import graphene, data_types
from py2neo import Node, Relationship
graph = graphene.get_database()


class Person(Resource):

    def __init__(self):
        #Request parser to get the params in a sexy way
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('person_id', type=str, location='json')
        self.reqparse.add_argument('email', type=str, required=True,
                                   location='json')
        self.reqparse.add_argument('name', type=str, location='json',
                                   required=True)
        self.reqparse.add_argument('gender', type=str, location='json')
        self.reqparse.add_argument('age', type=int, location='json')
        self.reqparse.add_argument('interested_in', type=list,
                                   location='json')
        self.reqparse.add_argument('height', type=int, location='json',
                                   default=160)
        self.reqparse.add_argument('likes')
        super(Person, self).__init__()
    
    @marshal_with(data_types.user_fields)
    def get(self, id):
        user = graph.find_one('Person', property_key='person_id',
                              property_value=id)
        if not user:
            abort(404, message="The requested user doesn't exist")
        return user.properties

    def put(self, id):
        args = self.reqparse.parse_args()
        user = graph.find_one('Person', property_key='person_id',
                              property_value=id)
        if user:
            user.properties['person_id']=id
            user.properties['email']=args['email']
            user.properties['name']=args['name']
            user.properties['gender']=args['gender']
            user.properties['age']=args['age']
            user.properties['interested_in']=args['interested_in']
            user.properties['height']=args['height']
            user.push()
            return ({"Put": user.properties})
        else:
            newPerson = Node(
                'Person',
                person_id=id,
                email=args['email'],
                name=args['name'],
                gender=args['gender'],
                age=args['age'],
                interested_in=args['interested_in'],
                height=args['height'],
                )

            try:
                graph.create(newPerson)
                return ({'Put': newPerson.properties}, 200)
            except:
                return ({'error': 'User was not created'}, 200)

    def post(self, id):
        args = self.reqparse.parse_args()
        user = graph.find_one('Person', property_key='person_id',
                              property_value= id)
        if user:
            return user.properties
        else:
            newPerson = Node(
                'Person',
                person_id=id,
                email=args['email'],
                name=args['name'],
                gender=args['gender'],
                age=args['age'],
                interested_in=args['interested_in'],
                height=args['height'],
                likes=args['likes'],
                )

            graph.create(newPerson)
            return ({'created': newPerson.properties}, 200)

    def delete(self, id):
        pass


