from flask import Flask, jsonify, abort, make_response, request
from flask.ext.restful import  Resource, reqparse, fields, marshal, marshal_with
from database import graphene, data_types
from py2neo import Node, Relationship

graph = graphene.get_database()

class TV_Show(Resource):

    def __init__(self):
        #Request parser to get the params in a sexy way
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('tvshow_id', type=str,
                                   required=True, location='json')
        self.reqparse.add_argument('title', type=str, required=True,
                                   location='json')
        self.reqparse.add_argument('year', type=str, location='json',
                                   required=True)
        self.reqparse.add_argument('genre', type=list, location='json')
        self.reqparse.add_argument('seasons', type=str, location='json')
        self.reqparse.add_argument('picture_url', type=str, location='json')
        super(TV_Show, self).__init__()
        
        
    @marshal_with(data_types.tvshow_fields)
    def get(self, id):
        
        tv_show = graph.find_one('TV_Show', property_key='tvshow_id',
                               property_value=id)
        if not tv_show:
            abort(404)
        return tv_show.properties

    def put(self, id):
        args = self.reqparse.parse_args()
        tvshow = graph.find_one('TV_Show', property_key='tvshow_id',
                              property_value=id)
        if tvshow:
            tvshow.properties['tvshow_id']=id
            tvshow.properties['title']=args['title']
            tvshow.properties['year']=args['year']
            tvshow.properties['genre']=args['genre']
            tvshow.properties['seasons']=args['seasons']
            tvshow.properties['picture_url'] = args ['picture_url']
            
            tvshow.push()
            return ({"Put": tvshow.properties})
        else:
            newTVshow = Node(
                'TV_Show',
                tvshow_id=id,
                title=args['title'],
                year=args['year'],
                genre=args['genre'],
                seasons=args['seasons'],
                picture_url=args['picture_url']
                )

            try:
                graph.create(newTVshow)
                return ({'Put tvshow': newTVshow.properties}, 200)
            except:
                return ({'error': 'tvshow was not created'}, 200)

    def delete(self, id):
        pass