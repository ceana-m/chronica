from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("login", views.login_view, name='login'),
    path("register", views.register, name='register'),
    path("logout", views.logout_view, name='logout'),

    path("books", views.books, name='books'),
    path("movies", views.movies, name='movies'),
    path("movies/<int:id>", views.movie_info, name='movie_info'),
    path("tv", views.tv, name='tv'),
    path("tv/<int:id>", views.tv_info, name='tv_info'),
    path("tv/<int:id>/seasons", views.tv_seasons, name='tv_seasons'),

    path("users/<str:user>/lists", views.user_lists, name='user_lists'),
    path("users/<str:user>/lists/<int:id>", views.list_view, name='list'),
    path("users/<str:user>/reviewed", views.reviewed, name='reviewed'),

    # API Methods
    # path("api/movie_review/<int:id>", views.movie_review, name='movie_review'),
    path("api/lists/<int:list_id>", views.lists_api, name='lists_api'),
    path("api/review/<str:media_type>/<int:media_id>", views.review_api, name='review_api'),
    path("api/media/<str:media_type>/<int:media_id>", views.media_api, name='media_api'),
]