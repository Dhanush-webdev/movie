from django.db import models
from django.contrib.auth.models import User

RATING_CHOICES = [(rating, str(rating)) for rating in range(1, 6)]


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.CharField(max_length=50)
    poster_image = models.ImageField(upload_to='posters/', blank=True, null=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        ratings = list(self.reviews.values_list('rating', flat=True))
        if not ratings:
            return 0
        return round(sum(ratings) / len(ratings), 1)


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('movie', 'user')
        ordering = ['-created_at']
