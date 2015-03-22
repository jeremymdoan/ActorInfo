from django.db import models, connection

class MoviesManager(models.Manager):
    def movies_amount(self, actor_id):
        cur = connection.cursor()
        cur.execute("""
            SELECT year, COUNT(1), AVG(rating)
            FROM actors_movies
            WHERE actor_id = %s
            and (year <> 0 or year is  not Null)
            and (rating <> 0 or rating is not null)
            GROUP BY actor_id, year
            ORDER BY year;""", [actor_id])
        return [row for row in cur.fetchall()]

    def movies_ratings(self, actor_id):
        cur = connection.cursor()
        cur.execute("""
            SELECT convert(movie_name using utf8), rating, year
            FROM actors_movies
            WHERE actor_id = %s
            and (year <> 0 or year is not Null)
            and (rating <> 0 or rating is not Null)
            ORDER BY year;""", [actor_id])
        return [row for row in cur.fetchall()]

    def actors_stats_1(self):
        cur = connection.cursor()
        cur.execute("""
            SELECT actor_id, convert(actor using utf8), avg(rating)
            FROM actors_movies a
            INNER JOIN actors_actor b
              ON b.id = a.actor_id
            WHERE (year <> 0 or year is not Null)
            and (rating <> 0 or rating is not Null)
            GROUP BY actor_id
            HAVING count(1) > 10
            ORDER BY avg(rating) desc
            LIMIT 25;""")
        return [row for row in cur.fetchall()]

    def actors_stats_2(self):
        cur = connection.cursor()
        cur.execute("""
            SELECT actor_id, convert(actor using utf8), count(1)
            FROM actors_movies a
            INNER JOIN actors_actor b
              ON a.actor_id = b.id
            WHERE (year <> 0 or year is not Null)
            AND (rating <> 0 or rating is not Null)
            GROUP BY actor_id
            ORDER BY count(1) desc
            LIMIT 25;""")
        return [row for row in cur.fetchall()]

class Actor(models.Model):
    actor = models.CharField(max_length=200)
    def __unicode__(self):
        return self.actor

class Movies(models.Model):
    actor = models.ForeignKey(Actor)
    movie_name = models.CharField(max_length=500)
    year = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits = 2, decimal_places=1, default=0.0)
    director = models.CharField(max_length=200)
    def __unicode__(self):
        return self.movie_name

    special_objects = MoviesManager()

# Create your models here.
