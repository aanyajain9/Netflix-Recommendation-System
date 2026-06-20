import pandas as pd


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