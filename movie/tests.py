from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from .forms import ReviewForm
from .models import Movie, Review


class MovieReviewTests(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title='Example Movie',
            description='A test movie.',
            release_date=date(2024, 1, 1),
            genre='Drama',
        )
        self.user = User.objects.create_user(username='reviewer', password='test-pass-123')

    def test_average_rating_uses_related_reviews(self):
        self.assertEqual(self.movie.average_rating(), 0)
        Review.objects.create(movie=self.movie, user=self.user, rating=4, comment='Good.')
        second_user = User.objects.create_user(username='another-reviewer', password='test-pass-123')
        Review.objects.create(movie=self.movie, user=second_user, rating=2, comment='Okay.')

        self.assertEqual(self.movie.average_rating(), 3.0)

    def test_review_form_rejects_ratings_outside_one_to_five(self):
        form = ReviewForm(data={'rating': '6', 'comment': 'Invalid rating.'})

        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_movie_detail_renders(self):
        response = self.client.get('/movies/{}/'.format(self.movie.pk))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/movie_details.html')
