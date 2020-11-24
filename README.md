# DSCI551-Project

## Dataset:
- [TMDB 5000 Movie Dataset](https://www.kaggle.com/tmdb/tmdb-movie-metadata)  
Download and save in `data/`

- [TMDB 5000 Movie Reviews in firebase](https://developers.themoviedb.org/3)


## Database:
- MySQL 8.0.21  
  - Dump Data  
  Using root user with no password. Please change the setting base on your preference.  
    - Start your mysql server:  
      - For mac users with homebrew install:  
        `brew services start mysql`
    - Create Schema:  
      `python src/create_schema.py`
    - Dump data:  
      `python src/dump_data.py`
- Firebase Realtime database


## WebFrame:
Django 3.1.3
- Go through the tutorial https://docs.djangoproject.com/en/3.1/intro/  
- Creating models (from MySQL server)  
  `python manage.py inspectdb > dsci551/models.py`  
  The model is not polished.
- Run Webserver  
  `cd web`  
  `python manage.py runserver`  
  Check the website http://localhost:8000/dsci551/home
