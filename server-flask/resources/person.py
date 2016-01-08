from flask import Flask, jsonify, abort, make_response, request
from flask.ext.restful import Resource, reqparse, fields, marshal
from database import graphene
from py2neo import Node, Relationship
graph = graphene.get_database()


class Person(Resource):

    def __init__(self):

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('person_id', type=str,
                                   required=True, location='json')
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

    def get(self, id):
        user = graph.find_one('Person', property_key='person_id',
                              property_value=str(id))
        if not user:
            abort(404)
        return user.properties

    def put(self, id):
        args = self.reqparse.parse_args()
        user = graph.merge_one('Person', 'person_id', args['person_id'])
        if user:
            return user.properties
        else:
            newPerson = Node(
                'Person',
                person_id=args['person_id'],
                email=args['email'],
                name=args['name'],
                gender=args['gender'],
                age=args['age'],
                interested_in=args['interested_in'],
                height=args['height'],
                )

            # add the likes: likes= args['likes']
            # validate if all the types and structure is correct:
            # user_object = marshal(new_user, data_types.user_fields)
            # print user_object
            # store.save_unique("Person", "person_id", toInsert.person_id, toInsert)
            # store.save(toInsert)

            try:
                graph.create(newPerson)
                return ({'created': newPerson.properties}, 200)
            except:
                return ({'error': 'User was not created'}, 200)

    def post(self, id):
        args = self.reqparse.parse_args()
        user = graph.find_one('Person', property_key='person_id',
                              property_value=args['person_id'])
        if user:
            return user.properties
        else:
            newPerson = Node(
                'Person',
                person_id=args['person_id'],
                email=args['email'],
                name=args['name'],
                gender=args['gender'],
                age=args['age'],
                interested_in=args['interested_in'],
                height=args['height'],
                likes=args['likes'],
                )

            # add the likes: likes= args['likes']
            # validate if all the types and structure is correct:
            # user_object = marshal(new_user, data_types.user_fields)
            # print user_object
            # store.save_unique("Person", "person_id", toInsert.person_id, toInsert)
            # store.save(toInsert)

            graph.create(newPerson)
            return ({'created': newPerson.properties}, 200)

    def delete(self, id):
        pass


