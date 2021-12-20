import pandas as pd

def getMovieTitle():
    genre_cols = ["genre_unknown", "Action", "Adventure", "Animation", "Children", "Comedy",
    "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror",
    "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]
    movies_cols = ['movie_id', 'title', 'release_date', "video_release_date", "imdb_url"] + genre_cols
    movies = pd.read_csv('u.item', sep='|', names=movies_cols, encoding='latin-1')
    return movies['title']
def getMovieUrl():
    url_cols = ["movie_id", "movie_url"]
    movieUrl = pd.read_csv('movie_poster.csv', header=None, names=url_cols)
    return movieUrl
def getMovieTuplte(movieIdList):
    Nmovie = 1682
    movieTPList = []
    mana = pd.read_csv('temp.csv')
    df = pd.read_csv('movielens_posters.csv')
    for n in movieIdList:
        temp = (mana['movie_title'][n], df['url'][n], mana['movie_id'][n] - 1)
        movieTPList.append(temp)
    return movieTPList