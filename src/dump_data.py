import pandas as pd
import mysql.connector
from collections import defaultdict


def extract_movies_info(credits_path, movies_path):
    cred = pd.read_csv(credits_path)
    movi = pd.read_csv(movies_path, keep_default_na=False)

    maxs = [0, 0, 0, 0, 0, 0, 0, 0]

    movie_dic = defaultdict(dict)
    genre_dic = defaultdict(dict)
    keyword_dic = defaultdict(dict)
    for _, row in cred.iterrows():
        movie_dic[row.movie_id]['id'] = row.movie_id
        movie_dic[row.movie_id]['title'] = row.title

    for _, row in movi.iterrows():
        movie_dic[row.id]['original_title'] = row.original_title
        movie_dic[row.id]['budget'] = row.budget
        movie_dic[row.id]['homepage'] = row.homepage
        movie_dic[row.id]['original_language'] = row.original_language
        movie_dic[row.id]['overview'] = row.overview
        movie_dic[row.id]['popularity'] = row.popularity

        raw_genre = eval(row.genres)
        for genre in raw_genre:
            genre_dic[genre['id']] = genre['name']

        keywords = eval(row.keywords)
        for keyword in keywords:
            keyword_dic[keyword['id']] = keyword['name']

    return movie_dic, genre_dic, keyword_dic


def dump_movies(movies):
    cnx = mysql.connector.connect(user='root', database='tmdb')
    cursor = cnx.cursor()

    add_movie = ("INSERT INTO movies "
                 "(id, title, original_title, budget, homepage, "
                 "original_language, overview, popularity) "
                 "VALUES (%(id)s, %(title)s, %(original_title)s, %(budget)s, "
                 "%(homepage)s, %(original_language)s, %(overview)s, "
                 "%(popularity)s)")

    for i in movies:
        cursor.execute(add_movie, movies[i])

    cnx.commit()

    cursor.close()
    cnx.close()


def dump_genres(genres):
    cnx = mysql.connector.connect(user='root', database='tmdb')
    cursor = cnx.cursor()

    add_genre = ("INSERT INTO genres "
                 "(id, name) "
                 "VALUES (%s, %s)")

    for i, name in genres.items():
        cursor.execute(add_genre, (i, name))

    cnx.commit()

    cursor.close()
    cnx.close()


def dump_keywords(keywords):
    cnx = mysql.connector.connect(user='root', database='tmdb')
    cursor = cnx.cursor()

    add_keyword = ("INSERT INTO keywords "
                   "(id, name) "
                   "VALUES (%s, %s)")

    for i, name in keywords.items():
        cursor.execute(add_keyword, (i, name))

    cnx.commit()

    cursor.close()
    cnx.close()

if __name__ == "__main__":
    credits_path = "data/TMDB/tmdb_5000_credits.csv"
    movies_path = "data/TMDB/tmdb_5000_movies.csv"
    movies, genres, keywords = extract_movies_info(credits_path, movies_path)
    dump_movies(movies)
    dump_genres(genres)
    dump_keywords(keywords)
