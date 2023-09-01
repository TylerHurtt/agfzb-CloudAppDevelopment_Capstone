from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarDealer
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
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
            context.error_message = 'Invalid username or password.'
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
    ids = []
    context = {}
    if request.method == "GET":
        url = f"{CLOUDANT_URL}/get-dealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        print('dealerships', dealerships)

        for dealer in dealerships:
            if dealer.id not in ids:
                ids.append(dealer.id)
                if 'dealerships' in context:
                    context['dealerships'].append(dealer)
                else:
                    context['dealerships'] = [dealer]

        # context['dealerships'] = get_dealers_from_cf(url)
        # # [DEPRECATED] Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, **kwargs):
    dealer_id = kwargs["dealer_id"]
    context = {}
    if request.method == "GET":
        url = f"{CLOUDANT_URL}/get-reviews-node"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        # Return a list of dealer short name
        context['reviews'] = reviews

    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    print('-----  add_review  -----')
    print('request', request)
    print('POST', request.POST)
    # authenticated = if request.user.is_authenticated

    # if not authenticated:
    #     return 'Not Authenticated'
    if request.method == 'GET':
        # Query cars based on the dealer id
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context = {
            'cars': cars,
            'dealer_id': dealer_id,
            'dealer_full_name': "test_dealership",
            'dealer': {"full_name": "test_dealership"},
        }
        return render(request, 'djangoapp/add_review.html', context)

    elif request.method == 'POST':
        review = dict()
        json_payload = dict()
        conent = request.POST.get('content')
        car_id = request.POST.get('car')[0]
        car = CarModel.objects.get(id=car_id)
        print('car', car)
        json_payload = {
            "name": request.POST.get('name'),
            "dealership": dealer_id,
            "review": request.POST.get('content'),
            "purchase": request.POST.get('purchasecheck') == 'on',
            "purchaseDate": datetime.strptime(request.POST.get('purchasedate'), '%m/%d/%Y').date(),
            "car_make": car.make.name,
            "car_model": car.name,
            "car_year": car.year,
        }
        url = f"{CLOUDANT_URL}/post-review-node"
        print('[ json_payload ]:', json_payload)
        response = post_request(url, json_payload, dealer_id=dealer_id)
        print('[ post ]:', response)
        return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
    return HttpResponseNotAllowed(['GET', 'POST'])
