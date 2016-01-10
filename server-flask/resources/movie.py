from flask import Flask, jsonify, abort, make_response, request
from flask.ext.restful import  Resource, reqparse, fields, marshal, marshal_with
from database import graphene, data_types
from py2neo import Node, Relationship

graph = graphene.get_database()

class Movie(Resource):

    def __init__(self):
        #Request parser to get the params in a sexy way
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('movie_id', type=str,
                                   required=True, location='json')
        self.reqparse.add_argument('title', type=str, required=True,
                                   location='json')
        self.reqparse.add_argument('year', type=str, location='json',
                                   required=True)
        self.reqparse.add_argument('genre', type=list, location='json')
        self.reqparse.add_argument('picture_url', type=str, location='json')
      
        super(Movie, self).__init__()
        
    @marshal_with(data_types.movie_fields)
    def get(self, id):
    
        movie = graph.find_one('Movie', property_key='movie_id',
                               property_value=str(id))
        if not movie:
            abort(404, message="The requested movie doesn't exist")
        return movie.properties

    def put(self, id):
        args = self.reqparse.parse_args()
        movie = graph.find_one('Movie', property_key='movie_id',
                              property_value=id)
        if movie:
            movie.properties['movie_id']=id
            movie.properties['title']=args['title']
            movie.properties['year']=args['year']
            movie.properties['genre']=args['genre']
            movie.properties['picture_url'] = args ['picture_url']

            movie.push()
            return ({"Put": movie.properties})
        else:
            newMovie = Node(
                'Movie',
                movie_id=id,
                title=args['title'],
                year=args['year'],
                genre=args['genre'],
                picture_url=args['picture_url']
                )

            try:
                graph.create(newMovie)
                return ({'Put Movie': newMovie.properties}, 200)
            except:
                return ({'error': 'Movie was not created'}, 200)

    def delete(self, id):
            pass