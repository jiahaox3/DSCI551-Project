import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'tmdb'

TABLES = {}
TABLES['movies'] = (
    "CREATE TABLE `movies` ("
    "  `id` int(11) NOT NULL ,"
    "  `title` varchar(100) NOT NULL,"
    "  `original_title` varchar(100) NOT NULL,"
    "  `budget` int(11) NOT NULL,"
    "  `homepage` varchar(300),"
    "  `original_language` varchar(2) NOT NULL,"
    "  `overview` varchar(10000) NOT NULL,"
    "  `popularity` float NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['genres'] = (
    "CREATE TABLE `genres` ("
    "  `id` int(11) NOT NULL ,"
    "  `name` varchar(20) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['genres_in_movies'] = (
    "CREATE TABLE `genres_in_movies` ("
    "  `genres_id` int(11) NOT NULL ,"
    "  `movie_id` int(11) NOT NULL,"
    "  PRIMARY KEY (`genres_id`, `movie_id`),"
    "  FOREIGN KEY (`genres_id`) REFERENCES `genres` (`id`),"
    "  FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`)"
    ") ENGINE=InnoDB")

TABLES['people'] = (
    "CREATE TABLE `people` ("
    "  `id` int(11) NOT NULL ,"
    "  `name` varchar(50) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['people_in_movies'] = (
    "CREATE TABLE `people_in_movies` ("
    "  `person_id` int(11) NOT NULL,"
    "  `movie_id` int(11) NOT NULL,"
    "  PRIMARY KEY (`person_id`, `movie_id`),"
    "  FOREIGN KEY (`person_id`) REFERENCES `people` (`id`),"
    "  FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`)"
    ") ENGINE=InnoDB")

TABLES['cast'] = (
    "CREATE TABLE `cast` ("
    "  `cast_id` int(11) NOT NULL ,"
    "  `movie_id` int(11) NOT NULL,"
    "  `character` varchar(50) NOT NULL,"
    "  `person_id` int(11) NOT NULL ,"
    "  PRIMARY KEY (`cast_id`, `movie_id`),"
    "  FOREIGN KEY (`person_id`) REFERENCES `people` (`id`),"
    "  FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`)"
    ") ENGINE=InnoDB")

TABLES['crew'] = (
    "CREATE TABLE `crew` ("
    "  `crew_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `movie_id` int(11) NOT NULL,"
    "  `department` varchar(50) NOT NULL,"
    "  `job` varchar(50) NOT NULL ,"
    "  `person_id` int(11) NOT NULL ,"
    "  PRIMARY KEY (`crew_id`, `movie_id`),"
    "  FOREIGN KEY (`person_id`) REFERENCES `people` (`id`),"
    "  FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`)"
    ") ENGINE=InnoDB")

TABLES['keywords'] = (
    "CREATE TABLE `keywords` ("
    "  `id` int(11) NOT NULL ,"
    "  `name` varchar(50) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['keywords_in_movies'] = (
    "CREATE TABLE `keywords_in_movies` ("
    "  `key_id` int(11) NOT NULL ,"
    "  `movie_id` int(11) NOT NULL,"
    "  PRIMARY KEY (`key_id`, `movie_id`),"
    "  FOREIGN KEY (`key_id`) REFERENCES `keywords` (`id`),"
    "  FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`)"
    ") ENGINE=InnoDB")


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS {} "
            "   DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


cnx = mysql.connector.connect(
    user='root', password='', host='localhost')
# creating database_cursor to perform SQL operation
cursor = cnx.cursor()

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()
