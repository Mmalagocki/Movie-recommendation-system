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


########################### MAIN ###########################


# my_columns = ['adult', 'id', 'original_title', 'popularity', 'video']
# df = pd.read_csv("result.csv", usecols=my_columns, sep=';')
# for line in df:
#     print(df)

train_columns = ['id', 'userid', 'movieid', 'rating']
users_db = read_csv("users.csv", train_columns)

movie_columns = ['id', 'tmdb', 'title']
movies_db = read_csv("movies.csv", movie_columns)


# watched_movies = []
# for index, line in users_db.iterrows():
#     print(index)
#     watched_movies.append(get_movie(line.movieid))
#
# with open('data.json', 'w') as outfile:
#     json.dump(watched_movies, outfile, indent=2)

f = open('data.json')
df = json.load(f)
# print(df)
# print(type(df))
# for line in df['adult']:
#     print(type(line))
#     print(line)
dataframe = pd.DataFrame.from_dict(df)
print(dataframe)
for line in dataframe.vote_count:
    print(line)
# for isadult in df['adult']:
#     print(isadult)
# for line in df:
#     print(line)

# df = json.loads(watched_movies)
# df.to_csv("movies_matrix.csv", sep=';')
# np.savetxt("foo.csv", watched_movies, delimiter=";")

#get_movie_id(movies_db, users_db)
# file_name = "task.csv"
# file = open(file_name, "r")
# array = create_rating(file)



# filter_values(df)
# array = create_rating(file)
# for line in array:
#     showing
#     print(line)
# print('Finished working')
