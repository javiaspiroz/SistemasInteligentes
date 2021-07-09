from tmdbv3api import Movie
from tmdbv3api import TMDb

def recomendacionExt(movieid):
    tmdb = TMDb()
    tmdb.api_key = 'bbb5fbe0beac436e41cb2dd89f9cc7b4'
    tmdb.language = 'es'
    tmdb.debug = True

    movie = Movie()
    m = movie.details(int(movieid))
    # print (m.title)
    # print (m.overview)
    # print (m.vote_average/2)
    rating= m.vote_average/2
    return rating