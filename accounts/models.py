from django.db import models

# Create your models here.


class User(models.Model):
    movie_id = models.IntegerField(db_column='id', primary_key=True)
