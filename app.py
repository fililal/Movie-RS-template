from flask import Flask, render_template, redirect, url_for, request
from poster_title import getMovieTuplte
 
app = Flask(__name__)

def getMovieTitle():
    genre_cols = [
    "genre_unknown", "Action", "Adventure", "Animation", "Children", "Comedy",
    "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror",
    "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]
    movies_cols = ['movie_id', 'title', 'release_date', "video_release_date", "imdb_url"] + genre_cols
 
@app.route('/')
def welcome():
    return redirect('/login')
 
 
@app.route('/home')
def home():
    return 'Login success!'
 
 
# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('movie', user=user))
    return render_template('login.html', error=error)

@app.route('/movie/<user>', methods=["POST", "GET"])
def movie(user=None):
    if request.method == "GET":
        movieList = getMovieTuplte([0, 1, 2, 3, 4, 5, 6])
        # movieList = [("https://images-na.ssl-images-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGdeQXVyNDQ2OTk4MzI@..jpg", "toy story")]
        return render_template('home.html', movie_cards=movieList)


 
 
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)