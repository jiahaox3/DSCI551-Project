# DSCI551-Project

## Dataset:
- [TMDB 5000 Movie Dataset](https://www.kaggle.com/tmdb/tmdb-movie-metadata)  
Download and save in `data/`

- [TMDB 5000 Movie Reviews in firebase](https://project-movie-reviews.firebaseio.com/)


## Database:
- MySQL 8.0.21  
- Dump Data  
Using root user with no password. Please change the setting base on your preference.  
  - Start your mysql server:  
    - For mac user:  
      `brew services start mysql`
  - Create Schema:  
    `python create_schema.py`
  - Dump data:  
    `python dump_data.py`
