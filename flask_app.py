from flask import Flask, render_template, request
import pickle
import requests
import os

from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

API_KEY = os.getenv("OMDB_API_KEY")


movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_movie_details(movie_name):

    url = f"https://www.omdbapi.com/?apikey={API_KEY}&t={movie_name}"

    response = requests.get(url)

    data = response.json()

    return data

def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x:x[1]
    )[1:6]

    recommendations=[]

    for i in movie_list:

        movie_name = movies.iloc[i[0]].title

        details = fetch_movie_details(movie_name)



        recommendations.append({

        "title": movie_name,

        "poster": details.get("Poster",""),

        "rating": details.get("imdbRating","N/A"),

        "genre": details.get("Genre","N/A"),

        "year": details.get("Year","N/A"),

        "plot": details.get("Plot","Not Available")

    })
@app.route('/', methods=['GET', 'POST'])
def home():

    recommendations=[]

    selected_movie=None

    if request.method=="POST":

        movie=request.form["movie"]

        recommendations=recommend(movie)

        selected_movie=fetch_movie_details(movie)

    return render_template(

    'index.html',

    movie_list=movies['title'].values,

    recommendations=recommendations,

    selected_movie=selected_movie
    
    )

if __name__ == "__main__":
    app.run(debug=True)