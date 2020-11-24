from django.shortcuts import render
from .models import Dsci551, Genres
from django.db import connection
import pyrebase
#from pyspark.sql import SparkSession
from .models import Movies

#spark = SparkSession \
    #.builder \
    #.appName("q1") \
    #.config("spark.some.config.option", "some-value") \
    #.getOrCreate()

#ids = spark.read.option("header","true").csv('movies_id.csv')


config = {
    'apiKey': "AIzaSyD-cFEFVd5wfcXc4AD6hCRiuf1id39yJpg",
    'authDomain': "project-movie-reviews.firebaseapp.com",
    'databaseURL': "https://project-movie-reviews.firebaseio.com/",
    'storageBucket': "project-movie-reviews.appspot.com"
  }

firebase = pyrebase.initialize_app(config)
db = firebase.database()
# Create your views here.

def dsci551_index(request):
    dsci551 = Dsci551.objects.all()
    context = {
	'dsci551': dsci551
    }
    return render(request, 'dsci551_index.html', context)

def dsci551_detail(request, pk):
    dsci551 = Dsci551.objects.get(pk=pk)
    context = {
 	'dsci551': dsci551
    }
    return render(request, 'dsci551_detail.html', context)

def dsci551(request):
    return render(request, 'dsci551.html', {})

def search(request):
    query = request.GET.get('input')
    if(query == None):
        query = "Star+Wars"
    #newColumns = ["id", "title"]

    #ids.toDF(*newColumns)

    query = query.replace('+', ' ')
    moviesID = Movies.objects.filter(title=query)
    answer = moviesID[0].id
    #answer = answer.first()[0]
    first_reviews = db.child("movie_reviews").child(answer).get().val()
    context = {
        "first_reviews": first_reviews,
        "nbar": "search"
    }
    return render(request, 'dsci551_search.html', context)

def home(request):
    if request.method == 'POST':
        # 'genre_selection'：the name in this <select name="genre_selection">
        genre_selected = int(request.POST.get('genre_selection'))
        movie_info = []
        with connection.cursor() as cursor:
            cursor.execute("select M.title, M.popularity, M.budget, GROUP_CONCAT(p.name SEPARATOR ', ') from "
                           "(SELECT m.id, m.title, m.popularity, m.budget "
                           "FROM tmdb.genres_in_movies g, tmdb.movies m "
                           "WHERE g.genres_id = %s AND g.movie_id=m.id) AS M, "
                           "(select c.movie_id, p.name "
                           "from people p, crew_in_movies c "
                           "where p.id=c.person_id AND job='Director') AS P "
                           "where P.movie_id = M.id "
                           "Group by M.id "
                           "order by M.popularity desc", [genre_selected])
            movie_info = cursor.fetchall()
        genre_list = Genres.objects.all()
        context = {
            'genre_list': genre_list,
            'genre_selected': genre_selected,
            'movie_info': movie_info,
            "nbar": "homepage"
        }
        return render(request, 'home.html', context)

    genre_list = Genres.objects.all()
    context = {
        'genre_list': genre_list,
        "nbar": "homepage"
    }
    return render(request, 'home.html', context)