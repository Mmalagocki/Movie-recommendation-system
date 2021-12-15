import struct

import pandas as pd
import random
import requests
import numpy as np
import json
import math
from bitarray import bitarray

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


def distance_between_vectors(v1, v2):
    print('hi')


def create_rating(file):
    for line in file:
        print(line.rstrip().replace("NULL", str(random.randint(0, 5))))
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


def get_movie_genres(dataframe):
    movies = []
    for elem in dataframe:
        for genre in elem:
            movies.insert(int(genre['id']), genre['id'])
    movies_dict = list(dict.fromkeys(movies))

    return movies_dict


def get_similarity(movies_array, movie_to_compare, genres_list):
    k = 5
    dist_array = []

    # genres
    # popularity
    # average_rating

    for index, elem in movie_to_compare.iterrows():
        for index, movie_from_array in movies_array.iterrows():
            dist = math.sqrt(
                0.001 * math.pow((elem.popularity - movie_from_array.popularity), 2) +
                0.01 * math.pow((elem.average_rating - movie_from_array.average_rating), 2) +
                math.pow(sum(
                            abs(
                                np.subtract(genres_dist(movie_from_array.genres, genres_list),
                                            genres_dist(elem.genres, genres_list))
                                )
                            ), 2
                        ))
            dist_array.append(dist)
    return dist_array


def genres_dist(movie_genres, genres_list):
    i = 0
    vector = [0] * len(genres_list)
    for genre in movie_genres:
        for genre_from_list in genres_list:
            if genre_from_list == genre['id']:
                vector[i] = 1
                # print('found it')
                i = 0
                break
            i += 1

    return vector


def get_recommended_movie(dataframe):
    print(dataframe.userid)

    
    # new = dataframe[['genres', 'popularity', 'vote_average']].copy()
    # genres_list = get_movie_genres(new.genres)
    # movies_array = []
    # first_movie = []
    # i = 0
    # for index, elem in new.iterrows():
    #     if i == 0:
    #         first_movie.append((elem.genres, elem.popularity, elem.vote_average))
    #         # first_movie.append(elem.genres)
    #         # first_movie.append(elem.popularity)
    #         # first_movie.append(elem.vote_average)
    #         first_movie_df = pd.DataFrame(first_movie, columns=['genres', 'popularity', 'average_rating'])
    #         i += 1
    #     else:
    #         movies_array.append((elem.genres, elem.popularity, elem.vote_average))
    #         movies_df = pd.DataFrame(movies_array, columns=['genres', 'popularity', 'average_rating'])
    #
    # # genres_dist(first_movie_df, genres_list)
    # get_similarity(movies_df, first_movie_df, genres_list)


def get_users_movies(userid):
    print(userid)

########################### MAIN ###########################


train_columns = ['id', 'userid', 'movieid', 'rating']
users_db = read_csv("users.csv", train_columns)

movie_columns = ['id', 'tmdb', 'title']
movies_db = read_csv("movies.csv", movie_columns)

task_columns = ['id', 'userid', 'movieid', 'rating']
recommendation_db = read_csv("task.csv", train_columns)

# print(recommendation_db)
f = open('data.json')
dictionary = json.load(f)

df = pd.DataFrame.from_dict(dictionary)
df.sort_values("imdb_id", inplace = True)
df = df.drop_duplicates(subset=['imdb_id'])

for index, new_watched_movie in recommendation_db.iterrows():
    get_recommended_movie(new_watched_movie)
