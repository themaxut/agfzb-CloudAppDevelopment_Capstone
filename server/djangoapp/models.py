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
        return f"{self.name} - {self.year.year}"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
# Not implemented yet

# <HINT> Create a plain Python class `DealerReview` to hold review data
# Not implemented yet
