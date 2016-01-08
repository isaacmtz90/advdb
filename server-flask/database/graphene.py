from py2neo import Graph, Node, Relationship

def get_database():
    graph = Graph('http://netflixandchill:Muidp457FqQDqgyJ4LQP@netflixandchill.sb02.stations.graphenedb.com:24789/db/data/')
    try:
        graph.schema.create_uniqueness_constraint("User", "person_id")
        graph.schema.create_uniqueness_constraint("Movie", "movie_id")
        graph.schema.create_uniqueness_constraint("TV_Show", "tvshow_id")
        return graph
    except:
        return graph