from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related moels
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


#  ===============[  VIEWS  ]===============[.

# Create an `about` view to render a static about page
def about(request):
    context = {}

    return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}

    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            redirect('djangoapp:index')
        else:
            constext.error_message = 'Invalid username or password.'
            return render(request, 'djangoapp/registration.html', context)
        return redirect('djangoapp:index')
    else:
        return render(request, 'djangoapp/registration.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request

    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}

    return render(request, 'djangoapp/registration.html', context)
CLOUDANT_URL = "https://us-south.functions.appdomain.cloud/api/v1/web/b3d2a768-1b07-436b-95ef-1fa81153d76e/dealership-package"
# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = f"{CLOUDANT_URL}/get-dealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


def get_dealer_details(request, **kwargs):
    dealer_id = kwargs["dealer_id"]

    if request.method == "GET":
        url = f"{CLOUDANT_URL}/get-dealerID-reviews-node"
        # Get dealers from the URL
        dealerships = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...