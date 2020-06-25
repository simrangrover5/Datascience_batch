import json
import pandas as pd
def filter():

    df1 = pd.read_csv("tmdb_5000_movies.csv")
    column = ['keywords','overview','production_companies','production_countries','budget','status','title','tagline', 'vote_average','vote_count']
    for i in column:
        df1.drop(i,axis=1,inplace=True)
    genre = []
    for i in df1['genres']:
        g = []
        l1 = json.loads(i)
        for j in l1:
            g.append(j['name'])
        genre.append(g)
        
    #print(genre)
    df1['genres'] = genre
    return df1

