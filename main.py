import pandas as pd
import random
import requests
import numpy as np
import json

########################### LIBRARIES ###########################


def filter_values(dataframe):
    for value in dataframe.adult:
        if type(value) != bool:
            value = False
            print('Had to change adult value according to ' + str(value) + ', bad value type ')

    for value in dataframe.id:
        if type(value) != int:
            raise ValueError('Wrong id provided')

    for value in dataframe.original_title:
        if type(value) != str:
            raise ValueError('Missing tittle')

    for value in dataframe.popularity:
        if type(value) != float:
            value = random.randint(0, 1000)
            print('Had to change adult value according to ' + str(value) + ', bad value type ')

    for value in dataframe.video:
        if type(value) != bool:
            value = False
            print('Had to change video'' value according to' + str(value) + ', bad value type ')
    print('Filtered movies')


def create_rating(file):
    for line in file:
        line = line.rstrip().replace("NULL", str(random.randint(0, 5)))
    print('Rendered rating')
    return file


def get_movie_id(movies_tmdb, user_movies):
    for outer_index, watched_movie in user_movies.iterrows():
        for inner_index, movie in movies_tmdb.iterrows():
            if movie.id == watched_movie.movieid:
                watched_movie.movieid = movie.tmdb
        print(outer_index)

    user_movies.reset_index(inplace=True, drop=True)
    user_movies.to_csv("users.csv", sep=';')


def read_csv(name, columns):
    df = pd.read_csv(name, usecols=columns, sep=';')

    return df


def get_movie(movieid):
    basic_request = 'https://api.themoviedb.org/3/movie/'
    api_key = '?api_key=cf33aca9a10a39801842ff5cd265cfe1'
    r = requests.get(basic_request + str(movieid) + api_key)
    if r.status_code == 200:
        movie = json.loads(r.text)
        return movie
    else:
        raise ValueError('Nie ma takiego id (:')

def get_movies_similarity(dataframe):
    new = dataframe[['genres', 'popularity', 'vote_average']].copy()
    print(new)


########################### MAIN ###########################

train_columns = ['id', 'userid', 'movieid', 'rating']
users_db = read_csv("users.csv", train_columns)

movie_columns = ['id', 'tmdb', 'title']
movies_db = read_csv("movies.csv", movie_columns)

f = open('data.json')
dictionary = json.load(f)

df = pd.DataFrame.from_dict(dictionary)
df.sort_values("imdb_id", inplace = True)
df = df.drop_duplicates(subset=['imdb_id'])

get_movies_similarity(df)


