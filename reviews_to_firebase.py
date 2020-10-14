import requests
import json

review_data = json.loads(open('TMDB_Movie_Reviews.json').read())
url = 'https://project-movie-reviews.firebaseio.com/movie_reviews.json'
response = requests.put(url,json=review_data)
print(response.text)
    
