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
    test = []
    for outer_index, watched_movie in user_movies.iterrows():
        for inner_index, movie in movies_tmdb.iterrows():
            if movie.id == watched_movie.movieid:
                watched_movie.movieid = movie.tmdb
        print(outer_index)
        test.append(watched_movie)

    print(test)
    test = pd.DataFrame(test, columns=['id', 'userid', 'movieid', 'rating'])
    test.reset_index(inplace=True, drop=True)
    test.to_csv("test.csv", sep=';')

def read_csv(name, columns):
    df = pd.read_csv(name, usecols=columns, sep=';')

    return df


def get_movie_from_api(movieid):
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
    print(movies_array.average_rating)
    print(movie_to_compare.average_rating)

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
    print('done')
    return vector


def get_watched_movie(movie_id, movies_df):
    list = []
    for index, movie_df in movies_df.iterrows():
        if movie_id == movie_df['id']:
            list.append((movie_df.genres, movie_df.popularity, movie_df.vote_average))
            return list

def get_seen_movie(movie_id, movies_df):
    for index, movie_df in movies_df.iterrows():
        if movie_id == movie_df['id']:
            return movie_df[['genres', 'popularity', 'vote_average']].copy()


def get_rating(user_id, users_db):
    rating = []
    for index, user in users_db.iterrows():
        if user.userid == user_id:
            rating.append(user.rating)

    return rating


def get_recommended_movie(new_watched_movie, users_db, movies_df, movies_genres_df):
    movies_ids = get_users_movies_ids(new_watched_movie.userid, users_db)
    recently_watched = get_watched_movie(new_watched_movie.movieid, movies_df)
    recently_watched_df = pd.DataFrame(recently_watched, columns=['genres', 'popularity', 'vote_average'])
    recently_watched_df['rating'] = np.nan
    previously_watched_movies = []
    rating = get_rating(new_watched_movie.userid, users_db)

    for index, previously_watched_movie in movies_ids.iterrows():
        previously_watched_movies.append(get_seen_movie(previously_watched_movie.movieid, movies_df))
    rating_df = pd.DataFrame(rating, columns=['rating'])
    previously_watched_movies_df = pd.DataFrame(previously_watched_movies, columns=['genres', 'popularity', 'vote_average'])
    previously_watched_movies_df['rating'] = rating_df['rating'].to_numpy()
    genres_list = get_movie_genres(movies_genres_df.genres)
    # movies_array = []
    # new_movie = []
    # i = 0
    # for index, elem in new.iterrows():
    #     print(elem)
    #     if i == 0:
    #         new_movie.append((elem.genres, elem.popularity, elem.vote_average))
    #         # first_movie.append(elem.genres)
    #         # first_movie.append(elem.popularity)
    #         # first_movie.append(elem.vote_average)
    #         print(new_movie)
    #         # new_movie_df = pd.DataFrame(new_movie, columns=['genres', 'popularity', 'average_rating'])
    #         i += 1
    #     else:
    #         sumaaa =1
    #         # movies_array.append((elem.genres, elem.popularity, elem.vote_average))
    #         # movies_df = pd.DataFrame(movies_array, columns=['genres', 'popularity', 'average_rating'])
    #
    # genres_dist(recently_watched_df.genres, genres_list)
    get_similarity(previously_watched_movies_df, recently_watched_df, genres_list)


def get_users_movies_ids(user_id, users_db):
    watched_movies = []

    for index, watched_movie in users_db.iterrows():
        if int(user_id) == watched_movie.userid:
            watched_movies.append(watched_movie.movieid)

    watched_movies = pd.DataFrame(watched_movies, columns=['movieid'])
    return watched_movies

########################### MAIN ###########################


train_columns = ['id', 'userid', 'movieid', 'rating']
users_db = read_csv("users.csv", train_columns)

movie_columns = ['id', 'tmdb', 'title']
movies_db = read_csv("movies.csv", movie_columns)

task_columns = ['id', 'userid', 'movieid', 'rating']
recommendation_db = read_csv("test.csv", task_columns)

f = open('data.json')
dictionary = json.load(f)

movies_df = pd.DataFrame.from_dict(dictionary)
movies_genres_df = movies_df.copy()
movies_genres_df.sort_values("imdb_id", inplace = True)
movies_genres_df = movies_genres_df.drop_duplicates(subset=['imdb_id'])

for index, new_watched_movie in recommendation_db.iterrows():
    get_recommended_movie(new_watched_movie, users_db, movies_df, movies_genres_df)
