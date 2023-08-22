from django.db import models
from django.utils.timezone import now

# Create your models here.


class CarMake(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # Add any other fields here if needed

    def __str__(self):
        return self.name


class CarModel(models.Model):
    CAR_TYPES = (
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('Coupe', 'Coupe'),
        ('Wagon', 'Wagon'),
        ('Exotic', 'Exotic'),
    )

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=255)
    car_type = models.CharField(max_length=50, choices=CAR_TYPES)
    year = models.DateField()

    def __str__(self):
        return f"{self.name}"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


class CarDealer:

    def __init__(self, address, city, state, full_name, id, lat, long, short_name, st, zip):
        # Dealer id
        self.id = id
        # Dealer city
        self.city = city
        # Dealer state
        self.state = state
        # Dealer st
        self.st = st
        # Dealer address
        self.address = address
        # Dealer zip
        self.zip = zip
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer Full Name
        self.full_name = full_name

    def __str__(self):
        return self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data


class DealerReview:

    def __init__(self, name, purchase, review, id, dealership, car_model, car_year, sentiment, purchase_date, car_make):
        # Dealer dealership
        self.dealership = dealership
        # Dealer name
        self.name = name
        # Dealer purchase
        self.purchase = purchase
        # Dealer review
        self.review = review
        # Dealer purchase_date
        self.purchase_date = purchase_date
        # Dealer car make
        self.car_make = car_make
        # Location car model
        self.car_model = car_model
        # Location car year
        self.car_year = car_year
        # Dealer sentiment
        self.sentiment = sentiment
        # Dealer id
        self.id = id

    def __str__(self):
        return "Review: " + str(self.review) + " Sentiment: " + str(self.sentiment) + " "
