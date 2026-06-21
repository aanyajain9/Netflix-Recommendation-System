import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk


df = pd.read_csv("data/netflix_titles.csv")

df = df[['title',
         'director',
         'cast',
         'listed_in',
         'description']]

print(df.head())

df.fillna("",inplace=True)
print(df.isnull().sum())

df['tags'] = (
    df['director'] + ' ' +
    df['cast'] + ' ' +
    df['listed_in'] + ' ' +
    df['description']
)

print(df[['title', 'tags']].head())

new_df = df[['title', 'tags']]

print(new_df.head())

new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

cv = CountVectorizer(
    max_features=5000,
    stop_words='english'
)

vectors = cv.fit_transform(new_df['tags']).toarray()

print(vectors.shape)

similarity = cosine_similarity(vectors)

print(similarity.shape)

def recommend(movie):

    movie_index = new_df[new_df['title'] == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    for i in movie_list:
        print(new_df.iloc[i[0]].title)

    
recommend("Ganglands")
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def stem(text):
    y = []

    for i in text.split():
        y.append(ps.stem(i))

    return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)