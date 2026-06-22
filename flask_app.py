from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for i in movie_list:
        recommendations.append(
            movies.iloc[i[0]].title
        )

    return recommendations

@app.route('/', methods=['GET', 'POST'])
def home():

    recommendations = []

    if request.method == 'POST':
        movie = request.form['movie']
        recommendations = recommend(movie)

    return render_template(
        'index.html',
        movie_list=movies['title'].values,
        recommendations=recommendations
    )

if __name__ == "__main__":
    app.run(debug=True)