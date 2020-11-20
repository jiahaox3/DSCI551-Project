import pandas as pd
import mysql.connector
from collections import defaultdict

USER = 'root'
PASSWORD = ''


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
        genre_ids = []
        for genre in raw_genre:
            genre_ids.append(genre['id'])
            genre_dic[genre['id']] = genre['name']
        movie_relation[row.id]['genres'] = genre_ids

        keywords = eval(row.keywords)
        keywords_ids = []
        for keyword in keywords:
            keywords_ids.append(keyword['id'])
            keyword_dic[keyword['id']] = keyword['name']
        movie_relation[row.id]['keywords'] = keywords_ids

    print("OK")
    return movie_dic, genre_dic, keyword_dic, movie_relation


def extract_people_info(credits_path):
    print("Extracting people infomation: ", end=' ', flush=True)
    cred = pd.read_csv(credits_path)
    cast_dic = defaultdict(dict)
    crew_dic = defaultdict(dict)
    for _, row in cred.iterrows():
        cast_list = eval(row.cast)
        crew_list = eval(row.crew)
        for cast in cast_list:
            cast_dic[cast['id']]['name'] = cast['name']
            cast_dic[cast['id']].setdefault('movies', set()).add(
                (row.movie_id, cast['character']))
        for crew in crew_list:
            crew_dic[crew['id']]['name'] = crew['name']
            # Person may have several jobs
            crew_dic[crew['id']].setdefault('movies', set()).add(
                (row.movie_id, crew['department'], crew['job']))

    print("OK")
    return cast_dic, crew_dic


def dump_movies(movies):
    try:
        print("Dumping movie : ", end=' ')
        cnx = mysql.connector.connect(
            user=USER, password=PASSWORD, database='tmdb')
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
        cnx = mysql.connector.connect(
            user=USER, password=PASSWORD, database='tmdb')
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
        cnx = mysql.connector.connect(
            user=USER, password=PASSWORD, database='tmdb')
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
        cnx = mysql.connector.connect(
            user=USER, password=PASSWORD, database='tmdb')
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
        cnx = mysql.connector.connect(
            user=USER, password=PASSWORD, database='tmdb')
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


def dump_people(cast, crew):
    try:
        print("Dumping people: ", end=' ', flush=True)
        cnx = mysql.connector.connect(
            user=USER, password=PASSWORD, database='tmdb')
        cursor = cnx.cursor()
        add_person = ("INSERT INTO people "
                      "(id, name) "
                      "VALUES (%s, %s)")
        for i in cast:
            cursor.execute(add_person, (i, cast[i]['name']))
        for i in crew:
            if i not in cast:  # some people are in both cast and crew
                cursor.execute(add_person, (i, crew[i]['name']))
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        cnx.commit()
        print("OK")

    cursor.close()
    cnx.close()


def dump_people_in_movies(cast, crew):
    try:
        print("Dumping people in movies: ", end=' ', flush=True)
        cnx = mysql.connector.connect(
            user=USER, password=PASSWORD, database='tmdb')
        cursor = cnx.cursor()
        add_cast_in_movies = ("INSERT INTO cast_in_movies "
                              "(person_id, movie_id, role) "
                              "VALUES (%s, %s, %s)")
        add_crew_in_movies = ("INSERT INTO crew_in_movies "
                              "(person_id, movie_id, department, job) "
                              "VALUES (%s, %s, %s, %s)")
        for i in cast:
            for movie_id, character in cast[i]['movies']:
                cursor.execute(add_cast_in_movies, (i, movie_id, character))
        for i in crew:
            for movie_id, depart, job in crew[i]['movies']:
                cursor.execute(add_crew_in_movies, (i, movie_id, depart, job))
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
    # cast, crew = extract_people_info(credits_path)
    # dump_movies(movies)
    # dump_genres(genres)
    dump_genres_in_movies(movie_relation)
    # dump_people(cast, crew)
    # dump_people_in_movies(cast, crew)
    # # Takes too long to finish:
    # dump_keywords(keywords)
    # dump_keywords_in_movies(movie_relation)
