from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("login", views.login_view, name='login'),
    path("register", views.register, name='register'),
    path("logout", views.logout_view, name='logout'),

    # path("search", views.search, name='search'),
    path("books", views.books, name='books'),
    path("movies", views.movies, name='movies'),
    path("movies/<int:id>", views.movie_info, name='movie_info'),
    path("tv", views.tv, name='tv'),
    path("tv/<int:id>", views.tv_info, name='tv_info'),

    path("users/<str:user>", views.user, name='user'),
    path("users/<str:user>/lists/<int:id>", views.list_view, name='list'),
]