from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from numpy import arange

from .confid import *
from .forms import *
from .models import *

import json
import requests


def index(request):
    url1 = "https://api.themoviedb.org/3/trending/movie/week?language=en-US"
    url2 = "https://api.themoviedb.org/3/trending/tv/week?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_TOKEN}"
    }
    m_response = requests.get(url1, headers=headers)
    m_data = m_response.json()
    t_response = requests.get(url2, headers=headers)
    t_data = t_response.json()

    return render(request, "tracker/index.html", {
        'movies': m_data['results'],
        'tv': t_data['results']
    })

@login_required(login_url='/login')
def user_lists(request, user):
    try:
        User.objects.get(username=user)
    except User.DoesNotExist:
        return render(request, "tracker/error.html")
    if request.method == 'POST':
        form = NewList(request.POST)
        if form.is_valid():
            List.objects.create(user=get_current_user(request), title=form.cleaned_data['title'], description=form.cleaned_data['description'])
    return render(request, "tracker/user_lists.html", {
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
    return get_info(request, id, 'movie')

def get_info(request, id, mtype):
    # Valid types are movie, tv
    url = f"https://api.themoviedb.org/3/{mtype}/{id}?language=en-U"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()
    try:
        media = Media.objects.get(obj_id=response_data['id'], media_type=mtype)
        review = Review.objects.get(user=get_current_user(request), media=media)
        old_review = NewReview(instance=review)
    except Review.DoesNotExist:
        review = 0
        old_review = NewReview()
    except Media.DoesNotExist:
        media = 0
        old_review = NewReview()

    # prev_review = Review.objects.get()
    if request.method == "POST":
        form = NewReview(request.POST)
        error = {
            'type': 'movie',
            'media': response_data,
            'message': 'Please enter a valid rating number (0.0 - 5.0 with 0.5 increments)',
            'review_form': form,
            'lists': List.objects.filter(user=get_current_user(request))
        }
        if form.is_valid():
            rating = form.cleaned_data['rating']
            text = form.cleaned_data['text']
            vals = arange(0.0, 5.1, 0.5)
            if rating not in vals:
                return render(request, "tracker/info.html", error)
            
            if media == 0:
                media = Media.objects.create(obj_id=response_data['id'], media_type=mtype, data=response_data)
                review = Review.objects.create(user=get_current_user(request), rating=rating, text=text, media=media)
            elif review == 0:
                review = Review.objects.create(user=get_current_user(request), rating=rating, text=text, media=media)
            else:
                review.rating = rating
                review.text = text
                review.save()

            return render(request, "tracker/info.html", {
                'type': mtype,
                'media': response_data,
                'review_form': NewReview(instance=review),
                'lists': List.objects.filter(user=get_current_user(request)),
                'show': True
            })
        else:
            return render(request, "tracker/info.html", error)

    return render(request, "tracker/info.html", {
        'type': mtype,
        'media': response_data,
        'review_form': old_review,
        'lists': List.objects.filter(user=get_current_user(request))
    })

def tv(request):
    return render(request, "tracker/content.html", {
        'type': 'TV Show'
    })

def tv_info(request, id):
    return get_info(request, id, 'tv')

def tv_seasons(request, id):
    url = f"https://api.themoviedb.org/3/tv/{id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    return render(request, "tracker/seasons.html", {
        'media': response.json()
    })

def list_view(request, user, id):
    try:
        list_obj = List.objects.get(pk=id)
    except List.DoesNotExist:
        return render(request, "tracker/error.html")
    return render(request, "tracker/list.html", {
        'person': user,
        'list': list_obj,
        'items': list_obj.media.all(),
    })

def reviewed(request, user):
    reviews = Review.objects.filter(user=get_current_user(request)).all()
    items = []
    for r in reviews:
        items.append(r.media)
    return render(request, "tracker/reviewed.html", {
        'person': user,
        'items': items,
    })

# Helper method
def get_current_user(request):
    return User.objects.get(username=request.user.username)

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
    
#API methods (based on prev assignments)

def lists_api(request, list_id):
    # Query for requested list
    try:
        list_obj = List.objects.get(pk=list_id)
    except List.DoesNotExist:
        return JsonResponse({"error": "List not found."}, status=404)

    # Return list attributes
    if request.method == "GET":
        return JsonResponse(list_obj.serialize())

    # Update 
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get('action') == 'edit':
            if data.get('title') is not None:
                list_obj.title = data["title"]
            if data.get('desc') is not None:
                list_obj.description = data["desc"]
            list_obj.save()
            return HttpResponse(status=204)
        

        try: 
            media = Media.objects.get(media_type=data.get('mediaType'), obj_id=data.get('obj_id'))
        except Media.DoesNotExist:
            return JsonResponse({
                "error ": "Media item does not exist."
            }, status=400)
        
        if data.get('action') in ['add', 'remove']:
            if data.get('mediaType') in ['movie', 'tv', 'book']:
                if data.get('obj_id') is not None:
                    if data.get('action') == 'add':
                        list_obj.media.add(media)
                    elif data.get('action') == 'remove':
                        list_obj.media.remove(media)
                else:
                    return JsonResponse({
                        "error": "Must provide a valid object id."
                    }, status=400)
            else:
                return JsonResponse({
                    "error": "Must provide a valid media type ('movie', 'tv', or 'book')."
                }, status=400)
        else:
            return JsonResponse({
                "error": "Must provide valid List action ('add', 'remove', 'edit')."
            }, status=400)
        return HttpResponse(status=204)
    
    elif request.method == "DELETE":
        list_obj.delete()
        return HttpResponse(status=204)

    #List must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
    
def review_api(request, media_type, media_id):
    try:
        media = Media.objects.get(media_type=media_type, obj_id=media_id)
        rev_obj = Review.objects.get(media=media)
    except Media.DoesNotExist:
        return JsonResponse({"error": "Media not found."}, status=404)
    except Review.DoesNotExist:
        if request.method == "POST":
            if data.get('rating') is not None:
                if data.get('text') is not None:
                    Review.objects.create(user=get_current_user(request), rating=data.get('rating'), text=data.get('text'), media=media)
                else:
                    Review.objects.create(user=get_current_user(request), rating=data.get('rating'), media=media)
            else:
                return JsonResponse({"error": "Must provide numerical rating."}, status=404)
        else:
            return JsonResponse({"error": "Review not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(rev_obj.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get('rating') is not None:
            rev_obj.rating = data["rating"]
        else:
            return JsonResponse({
                "error": "Must provide a rating for the review."
            }, status=400)
        if data.get('text') is not None:
            rev_obj.text = data["text"]
        rev_obj.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET or POST request required."
        }, status=400)
    
@ensure_csrf_cookie
def media_api(request, media_type, media_id):
    try:
        media = Media.objects.get(media_type=media_type, obj_id=media_id)
    except Media.DoesNotExist:
        if request.method == "POST":
            data = json.loads(request.body)
            if data.get('obj_id') is not None or data.get('media_type') is not None:
                if data.get('mediaType') in ['movie', 'tv', 'book']:
                    if data.get('data') is not None:
                        Media.objects.create(obj_id=data['obj_id'], media_type=data["mediaType"], data=json.loads(data['data']))
                        return HttpResponse(status=204)
                    else:
                        return JsonResponse({
                            "error": "Must provide data to be stored."
                        }, status=400)
                else:
                    return JsonResponse({
                        "error": "Must provide a valid media type ('movie', 'tv', or 'book')."
                    }, status=400)
            else:
                return JsonResponse({
                    "error": "Must provide an object id for API use as well as a media type."
                }, status=400)
        else:
            return JsonResponse({"error": "Media item not found. POST request required."}, status=404)
    
    # If it already exists don't do anything
    if request.method == "POST":
        return HttpResponse(status=204)

    if request.method == "GET":
        return JsonResponse(media.serialize())

    else:
        return JsonResponse({
            "error": "GET or POST request required."
        }, status=400)
        
