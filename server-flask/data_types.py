from flask.ext.restful import fields
import json
#types used for formatting  the data
movie_fields = {
    'movie_id': fields.String,
    'title': fields.String,
    'year': fields.Integer,
    'genre': fields.String
    }

tvshow_fields = {
    'tvshow_id': fields.String,
    'title': fields.String,
    'year': fields.Integer,
    'seasons': fields.Integer,
    'genre': fields.String
    }

likes_fields = \
    {'movies_liked': fields.List(fields.Nested(movie_fields)),
     'tvshows_liked': fields.List(fields.Nested(tvshow_fields))}

user_fields = {
    'person_id': fields.String,
    'email': fields.String,
    'name': fields.String,
    'age': fields.Boolean,
    'gender': fields.String,
    'interested_in': fields.List(fields.String),
    'height': fields.String,
    'likes': fields.Nested(likes_fields)
    }
    
user_field = {
    'person_id': fields.String,
    'name': fields.String,
    'age': fields.Boolean,
    'gender': fields.String,
    'interested_in': fields.List(fields.String),
    'height': fields.String,
    'weight': fields.String,
    'likes': fields.Nested(likes_fields)
    }


class Person(object):
    def __init__(self, person_id=None, email=None,name=None, age=None, gender=None, interested_in=[], height=None, likes=None):
        self.person_id =person_id
        self.email = email
        self.name=name
        self.age=age
        self.gender=gender
        self.interested_in= interested_in
        self.height= height
        self.likes= likes
    def  __str__(self):
        return self.person_id+ self.name
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
class Movie(object):
    def __init__(self, movie_id=None, title=None, year=None, genre=None):
        self.movie_id =movie_id
        self.title=title
        self.year=year
        self.genre=genre
      
    def  __str__(self):
        return self.movie_id+ self.title
    
class TVShow(object):
    def __init__(self, tvshow_id=None, title=None, year=None, genre=None, seasons =None):
        self.tvshow_id =tvshow_id
        self.title=title
        self.year=year
        self.genre=genre
        self.seasons= seasons
      
    def  __str__(self):
        return self.tvshow_id+ self.title
    
class Likes(object):
    def __init__(self, movies_liked=[], tvshows_liked=[]):
        self.movies_liked =movies_liked
        self.tvshows_liked=tvshows_liked      
      

