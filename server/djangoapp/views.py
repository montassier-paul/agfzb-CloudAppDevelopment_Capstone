from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)




# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


# Create a `login_request` view to handle sign in request
def login_request(request):
    print("Login Request")
    if request.method == "POST":
        username = request.POST['username']
        print("Login: Username", username)
        password = request.POST['psw']
        print("Login: Password", password)
        user = authenticate(username=username, password=password)
        if user is not None:
            print("Login: User", User)
            login(request, user)
            return redirect("djangoapp:index")
       

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    
    logout(request)
    return redirect("djangoapp:index")


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    print("Registartion Request")
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    if request.method == "POST":
        username = request.POST['username']
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        password = request.POST['psw']
        userResult = User.objects.filter(username=username)
        if len(userResult) == 0:
            user = User.objects.create_user(username=username, first_name=firstName, last_name=lastName, password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://c64b0b09.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        
        context = {
            "dealerships": dealerships,
            "dealer_name": dealer_names
        }

        # return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)

def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://c64b0b09.eu-gb.apigw.appdomain.cloud/api/review"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context = {
            "reviews": reviews,
            "dealer_id": dealer_id
        }
        print(context)
        sentiments = ' '.join([review.sentiment for review in reviews])       
        # return render(request, 'djangoapp/dealer_details.html', context)
        return HttpResponse(sentiments)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

