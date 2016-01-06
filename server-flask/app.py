#!Scripts/python
from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource
from py2neo import Graph, Node, Relationship

app = Flask(__name__,static_url_path="")
api = Api(app)

graph = Graph("http://netflixandchill:Muidp457FqQDqgyJ4LQP@netflixandchill.sb02.stations.graphenedb.com:24789/db/data/")
#graph.schema.create_uniqueness_constraint("User", "id")
#graph.schema.create_uniqueness_constraint("Movie", "id")
#graph.schema.create_uniqueness_constraint("TV_Show", "id")
print 'connected to graph'


def serialize_node(node):
    nodestruct = {'labels': [], 'properties': [node.properties]}
    return nodestruct
   
    

class User(Resource):
    def get(self, id):
        
        user = graph.find_one("Person", property_key='person_id', property_value=id)
        if not user:
            abort(404)
        return  serialize_node(user)
    
    def put(self, id):
        bob = Node("Person", name="Bob", person_id = id)
        graph.create(bob)
        pass
    
    def delete(self,id):
        pass
    

class Movie(Resource):
    def get(self, id):         
        movie = graph.find_one("Movie", id=id)
        if len(movie)==0:
            abort(404)
        return movie
    
    def put(self, id):       
        pass
    
    def delete(self,id):
        pass
    
class TV_Show(Resource):
    def get(self, id):
        tvshow = graph.find_one("TV_Show", id=id)
        if len(tvshow)==0:
            abort(404)
        return tvshow
    
    def put(self, id):       
        pass
    
    def delete(self,id):
        pass

class TestAPI(Resource):
    def get(self, id):
        return { 'id_is': id }
    
    def put(self, id):
       
        pass
    
    def delete(self,id):
        pass
    
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
    
api.add_resource(User, '/users/<int:id>', endpoint='users')
api.add_resource(Movie, '/movies/<int:id>', endpoint='movies')
api.add_resource(TV_Show, '/tv_shows/<int:id>', endpoint='tv_show')
api.add_resource(TestAPI, '/tests/<int:id>', endpoint='test')
print 'resource url created'

if __name__ == '__main__':
    app.run(debug=True)
                 