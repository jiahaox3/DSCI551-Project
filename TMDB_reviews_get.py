import requests
import json
import csv
from requests.auth import HTTPBasicAuth
import csv

movie_id=[]
with open('TMDB_Movie_IDs.csv', newline = '') as csvfile:
     spamreader=csv.reader(csvfile,delimiter=' ',quotechar='|')
     for row in spamreader:
         movie_id.append(row[0])

#TMDB API Key: acb33c8308946ca9146d845ef3fb67ba
#API_key ='acb33c8308946ca9146d845ef3fb67ba'

reviews = {}
for id in movie_id[1:]:
    url = 'https://api.themoviedb.org/3/movie/'+str(id)+'/reviews?api_key=acb33c8308946ca9146d845ef3fb67ba&language=en-US&page=1'
    response = requests.get(url)
    review = json.loads(response.text)
    try:
       reviews[str(id)]=review['results']
    except:
       print(id)

with open('TMDB_Movie_Reviews.json','w') as fp:
     json.dump(reviews,fp)


