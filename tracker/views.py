from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import *

import requests
from .confid import *

def index(request):
    return render(request, "tracker/index.html")

# def search(request):
#     return render(request, "tracker/content.html", {
#         'type': 'Book'
#     })

@login_required(login_url='/login')
def user(request, user):
    try:
        User.objects.get(username=user)
    except User.DoesNotExist:
        return render(request, "tracker/error.html")
    if request.method == 'POST':
        form = NewList(request.POST)
        if form.is_valid():
            List.objects.create(user=User.objects.get(username=request.user.username), title=form.cleaned_data['title'], description=form.cleaned_data['description'])
    return render(request, "tracker/user.html", {
        'person': user,
        'form': NewList(),
        'lists': List.objects.filter(user=User.objects.get(username=user))
    })

def books(request):
    return render(request, "tracker/content.html", {
        'type': 'Book'
    })

def movies(request):
    return render(request, "tracker/content.html", {
        'type': 'Movie'
    })

def movie_info(request, id):
    url = f"https://api.themoviedb.org/3/movie/{id}?language=en-U"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_TOKEN}"
    }
    response = requests.get(url, headers=headers)

    return render(request, "tracker/info.html", {
        'type': 'movie',
        'media': response.json()
    })

def tv(request):
    return render(request, "tracker/content.html", {
        'type': 'TV Show'
    })

def tv_info(request, id):
    url = f"https://api.themoviedb.org/3/tv/{id}?language=en-U"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_TOKEN}"
    }
    response = requests.get(url, headers=headers)

    return render(request, "tracker/info.html", {
        'type': 'tv',
        'media': response.json()
    })

def list_view(request, user, id):
    try:
        list_obj = List.objects.get(pk=id)
    except List.DoesNotExist:
        return render(request, "tracker/error.html")
    return render(request, "tracker/list.html", {
        'person': user,
        'list': list_obj
    })

# Code below and their corresponding templates adapted from previous assignments
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "tracker/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "tracker/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "tracker/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "tracker/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tracker/register.html")