import pandas as pd
import mysql.connector
from collections import defaultdict


def extract_movies_info(credits_path, movies_path):
    print("Extracting movie infomation: ", end=' ', flush=True)
    cred = pd.read_csv(credits_path)
    movi = pd.read_csv(movies_path, keep_default_na=False)

    movie_dic = defaultdict(dict)
    genre_dic = defaultdict(dict)
    keyword_dic = defaultdict(dict)
    movie_relation = defaultdict(dict)
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
        movie_relation[row.id]['genres'] = genre_dic.keys()

        keywords = eval(row.keywords)
        for keyword in keywords:
            keyword_dic[keyword['id']] = keyword['name']
        movie_relation[row.id]['keywords'] = keyword_dic.keys()

    print("OK")
    return movie_dic, genre_dic, keyword_dic, movie_relation


def extract_people_info(credits_path):
    print("Extracting people infomation: ", end=' ', flush=True)
    cred = pd.read_csv(credits_path)
    people_dic = defaultdict(dict)
    for _, row in cred.iterrows():
        cast_list = eval(row.cast)
        crew_list = eval(row.crew)
        for cast in cast_list:
            people_dic[cast['id']]['name'] = cast['name']
            people_dic[cast['id']].setdefault(
                'movies', set()).add(row.movie_id)
        for crew in crew_list:
            people_dic[crew['id']]['name'] = crew['name']
            # Person may have several jobs
            people_dic[crew['id']].setdefault(
                'movies', set()).add(row.movie_id)

    print("OK")
    return people_dic


def dump_movies(movies):
    try:
        print("Dumping movie : ", end=' ')
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
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        cnx.commit()
        print("OK")

    cursor.close()
    cnx.close()


def dump_genres(genres):
    try:
        print("Dumping generes: ", end=' ')
        cnx = mysql.connector.connect(user='root', database='tmdb')
        cursor = cnx.cursor()
        add_genre = ("INSERT INTO genres "
                     "(id, name) "
                     "VALUES (%s, %s)")
        for i, name in genres.items():
            cursor.execute(add_genre, (i, name))
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        cnx.commit()
        print("OK")

    cursor.close()
    cnx.close()


def dump_keywords(keywords):
    try:
        print("Dumping keywords: ", end=' ')
        cnx = mysql.connector.connect(user='root', database='tmdb')
        cursor = cnx.cursor()

        add_keyword = ("INSERT INTO keywords "
                       "(id, name) "
                       "VALUES (%s, %s)")

        for i, name in keywords.items():
            cursor.execute(add_keyword, (i, name))
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        cnx.commit()
        print("OK")

    cursor.close()
    cnx.close()


def dump_genres_in_movies(movies):
    try:
        print("Dumping generes relationship: ", end=' ')
        cnx = mysql.connector.connect(user='root', database='tmdb')
        cursor = cnx.cursor()
        add_genre_in_movies = ("INSERT INTO genres_in_movies "
                               "(genres_id, movie_id) "
                               "VALUES (%s, %s)")
        for i in movies:
            for genre in movies[i]['genres']:
                cursor.execute(add_genre_in_movies, (genre, i))
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        cnx.commit()
        print("OK")

    cursor.close()
    cnx.close()


def dump_keywords_in_movies(movies):
    try:
        print("Dumping keywords relationship: ", end=' ', flush=True)
        cnx = mysql.connector.connect(user='root', database='tmdb')
        cursor = cnx.cursor()
        add_keyword_in_movies = ("INSERT INTO keywords_in_movies "
                                 "(key_id, movie_id) "
                                 "VALUES (%s, %s)")
        for i in movies:
            for keyword in movies[i]['keywords']:
                cursor.execute(add_keyword_in_movies, (keyword, i))
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        cnx.commit()
        print("OK")

    cursor.close()
    cnx.close()


def dump_people(people):
    try:
        print("Dumping people: ", end=' ', flush=True)
        cnx = mysql.connector.connect(user='root', database='tmdb')
        cursor = cnx.cursor()
        add_keyword_in_movies = ("INSERT INTO people "
                                 "(id, name) "
                                 "VALUES (%s, %s)")
        for i in people:
            cursor.execute(add_keyword_in_movies, (i, people[i]['name']))
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        cnx.commit()
        print("OK")

    cursor.close()
    cnx.close()


def dump_people_in_movies(people):
    try:
        print("Dumping people in movies: ", end=' ', flush=True)
        cnx = mysql.connector.connect(user='root', database='tmdb')
        cursor = cnx.cursor()
        add_keyword_in_movies = ("INSERT INTO people_in_movies "
                                 "(person_id, movie_id) "
                                 "VALUES (%s, %s)")
        for i in people:
            for movie_id in people[i]['movies']:
                cursor.execute(add_keyword_in_movies, (i, movie_id))
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        cnx.commit()
        print("OK")

    cursor.close()
    cnx.close()


if __name__ == "__main__":
    credits_path = "data/TMDB/tmdb_5000_credits.csv"
    movies_path = "data/TMDB/tmdb_5000_movies.csv"
    movies, genres, keywords, movie_relation = extract_movies_info(
        credits_path, movies_path)
    people = extract_people_info(credits_path)
    dump_movies(movies)
    dump_genres(genres)
    dump_genres_in_movies(movie_relation)
    dump_people(people)
    dump_people_in_movies(people)
    # dump_keywords(keywords)
    # dump_keywords_in_movies(movie_relation)
