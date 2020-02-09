from django.db import models

# Create your models here.


class Movie(models.Model):
    movie_id = models.IntegerField(db_column='movie_id',primary_key=True)
    category_id = models.IntegerField(null=True)
    director = models.CharField(max_length=150, null=True)
    title = models.CharField(max_length=300, null=True)
    year_released = models.IntegerField(max_length=4, null=True)

    class Meta:
        db_table = "movies"

