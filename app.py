from flask import Flask, render_template, redirect, url_for, request
from poster_title import getMovieTuplte
import engine
import json
 
app = Flask(__name__)
model = engine.process()
 
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
        if request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('movie', user=user))
    return render_template('login.html', error=error)

@app.route('/movie/<user>', methods=["POST", "GET"])
def movie(user=None, movie=None):
    if request.method == "GET":
        recList = model.recommend(int(user))
        movieList = getMovieTuplte(recList)
        return render_template('home.html', movie_cards=movieList, user=user)


@app.route('/movie/<user>/<movie>', methods=["POST", "GET"])
def watchMovie(user=None, movie=None):
    if request.method == "GET":
        movieList = []
        movieList.append(int(movie))
        movieInfors = getMovieTuplte(movieList)
        for movieInfor in movieInfors:
            title, url, idM = movieInfor
        return render_template('watchMovie.html', title=title, urlimg=url, user=user, movie=movie)

@app.route('/rate', methods=["POST"])
def rateUp():
    rating = request.form['rating']
    user = request.form['user']
    movie = request.form['movie']
    # print(user, movie, rating)
    model.addRating(user=int(user), movie=int(movie), rating=int(rating))
    return render_template('login.html')

@app.route('/search/<user>', methods=["POST"])
def search(user=None):
    # result = request.form['searchResults']
    # print(result)
    if request.method == "POST":
        # print(request.form['searchResults'])
        movieId = int(request.form['movieId']) - 1
        return redirect(url_for('watchMovie', user=int(user), movie=movieId))

 
 
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)