import pandas as pd
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nltk.stem.porter import PorterStemmer

# -------------------------------
# Load Dataset
# -------------------------------

df = pd.read_csv("data/netflix_titles.csv")

# -------------------------------
# Select Required Columns
# -------------------------------

df = df[['title',
         'director',
         'cast',
         'listed_in',
         'description']]

# -------------------------------
# Handle Missing Values
# -------------------------------

df.fillna("", inplace=True)

# -------------------------------
# Create Tags Column
# -------------------------------

df['tags'] = (
    df['director'] + ' ' +
    df['cast'] + ' ' +
    df['listed_in'] + ' ' +
    df['description']
)

# -------------------------------
# Create New DataFrame
# -------------------------------

new_df = df[['title', 'tags']].copy()

# -------------------------------
# Convert to Lowercase
# -------------------------------

new_df['tags'] = new_df['tags'].apply(
    lambda x: x.lower()
)

# -------------------------------
# Stemming
# -------------------------------

ps = PorterStemmer()

def stem(text):
    y = []

    for word in text.split():
        y.append(ps.stem(word))

    return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

# -------------------------------
# Text Vectorization
# -------------------------------

cv = CountVectorizer(
    max_features=5000,
    stop_words='english'
)

vectors = cv.fit_transform(
    new_df['tags']
).toarray()

# -------------------------------
# Similarity Matrix
# -------------------------------

similarity = cosine_similarity(vectors)

# -------------------------------
# Save Files
# -------------------------------

pickle.dump(
    new_df,
    open('movies.pkl', 'wb')
)

pickle.dump(
    similarity,
    open('similarity.pkl', 'wb')
)

# -------------------------------
# Recommendation Function
# -------------------------------

def recommend(movie):

    movie_index = new_df[
        new_df['title'] == movie
    ].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    print("\nRecommended Movies:\n")

    for i in movie_list:
        print(
            new_df.iloc[i[0]].title
        )

# -------------------------------
# Test
# -------------------------------

recommend("Ganglands")
