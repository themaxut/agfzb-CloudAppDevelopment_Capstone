from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarMake, CarModel
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .restapis import get_dealers_from_cf, post_request, get_dealer_reviews_from_cf, get_request
from datetime import datetime
import logging
import json
import requests

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    return render(request, 'djangoapp/index.html')


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request


def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'djangoapp/login.html')


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request


def registration_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Assuming you also have an email field in the signup form.
        email = request.POST.get('email')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = User.objects.create_user(
                username=username, password=password, email=email)
            login(request, user)
            return redirect('djangoapp:index')
    return render(request, 'djangoapp/registration.html')

# Update the `get_dealerships` view to render the index page with a list of dealerships


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {
        "page": "index"
    }
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/faa4e27a-4308-4e63-99f9-80ea8ab01d4f/dealership-package/get-dealership.json"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealerships"] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {
        "page": "dealer_details",
        "dealer_id": dealer_id
    }
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/faa4e27a-4308-4e63-99f9-80ea8ab01d4f/dealership-package/get-review-by-dealership.json"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context["reviews"] = reviews

        url = "https://us-south.functions.appdomain.cloud/api/v1/web/faa4e27a-4308-4e63-99f9-80ea8ab01d4f/dealership-package/get-dealership.json"
        dealerships = get_dealers_from_cf(url)
        dealership = (
            element for element in dealerships if element.id == dealer_id)
        context["dealership"] = next(dealership)

        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...


def add_review(request, dealer_id):
    user = request.user
    context = {
        "page": "add_review",
        "dealer_id": dealer_id
    }
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/faa4e27a-4308-4e63-99f9-80ea8ab01d4f/dealership-package/get-review-by-dealership.json"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context["reviews"] = reviews

        url = "https://us-south.functions.appdomain.cloud/api/v1/web/faa4e27a-4308-4e63-99f9-80ea8ab01d4f/dealership-package/get-dealership.json"
        dealerships = get_dealers_from_cf(url)
        dealership = (
            element for element in dealerships if element.id == dealer_id)
        context["dealership"] = next(dealership)

        all_cars = CarModel.objects.all()
        cars = []
        for car in all_cars:
            if car.dealer_id == dealer_id:
                cars.append(car)
        context["cars"] = (cars)

        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        # Gather data from the form
        new_review = {
            "id": "",
            "name": user.username,
            "dealership": dealer_id,
            "review": request.POST["content"],
            "purchase": str(request.POST.get("purchasecheck", "") == "on").lower(),
            "purchase_date": datetime.strptime(request.POST["purchasedate"],
                                               '%Y-%m-%d').strftime('%d/%m/%Y'),
            "review_time": datetime.utcnow().isoformat()  # Review time in ISO format
        }

        # Find the selected car from the dropdown
        selected_car = CarModel.objects.get(id=int(request.POST["car"]))
        new_review["car_make"] = selected_car.car_make.name
        new_review["car_model"] = selected_car.name
        new_review["car_year"] = selected_car.year.strftime("%Y")

        # Send the review data to the Cloud Function
        json_payload = {"review": new_review}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/faa4e27a-4308-4e63-99f9-80ea8ab01d4f/dealership-package/post-review"
        result = post_request(url, json_payload)

        # Redirect to dealer details page
        return redirect('djangoapp:dealer_details', dealer_id=dealer_id)

    # Render the template (for GET request)
    return render(request, 'djangoapp/add_review.html', context)
