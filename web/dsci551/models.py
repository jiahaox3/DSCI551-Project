from django.db import models

# Create your models here.
class Dsci551(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=20)
    image = models.FilePathField(path="/img")
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class CastInMovies(models.Model):
    person = models.ForeignKey('People', models.DO_NOTHING)
    movie = models.ForeignKey('Movies', models.DO_NOTHING)
    role = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'cast_in_movies'


class CrewInMovies(models.Model):
    person = models.ForeignKey('People', models.DO_NOTHING)
    movie = models.ForeignKey('Movies', models.DO_NOTHING)
    department = models.CharField(max_length=50)
    job = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'crew_in_movies'


class Dsci551Dsci551(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=20)
    image = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'dsci551_dsci551'


class Genres(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'genres'

    def __str__(self):
        return self.name


class GenresInMovies(models.Model):
    genres = models.ForeignKey(Genres, models.DO_NOTHING)
    movie = models.ForeignKey('Movies', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'genres_in_movies'


class Keywords(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'keywords'


class KeywordsInMovies(models.Model):
    key = models.ForeignKey(Keywords, models.DO_NOTHING)
    movie = models.ForeignKey('Movies', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'keywords_in_movies'


class Movies(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    budget = models.IntegerField()
    homepage = models.CharField(max_length=300, blank=True, null=True)
    original_language = models.CharField(max_length=2)
    overview = models.CharField(max_length=10000)
    popularity = models.FloatField()

    class Meta:
        managed = False
        db_table = 'movies'


class People(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'people'
