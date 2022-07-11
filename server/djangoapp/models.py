from django.db import models
from django.utils.timezone import now
import datetime


# Create your models here.


class CarMake(models.Model):
    name = models.CharField(null=False, max_length=20, primary_key=True)
    desc = models.TextField()
    def __str__(self):
        return "Name: " + self.name + "," \
                "Description: " + self.desc


class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(null=False)
    name = models.CharField(null=False, max_length=20, primary_key=True)
    SUV = 'suv'
    SEDAN = 'sedan'
    WAGON = 'wagon'
    JEEP = 'jeep'
    TYPE_CHOICES = [
        (SUV, 'SUV'),
        (SEDAN, 'Sedan'),
        (WAGON, 'Wagon'),
        (JEEP, 'Jeep')
    ]
    model_type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    year = models.IntegerField(default=datetime.date.today().year) 
    
    def __str__(self):
        return "Make: " + self.make.name + "," \
                "Name: " + self.name + "," \
                "Year: " + str(self.year) + "," \
                "Type: " + self.model_type + "," \
                "Dealer ID: " + str(self.dealer_id)





# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id_, lat, long_, short_name, st,state, zip_):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id_
        self.lat = lat
        self.long = long_
        self.short_name = short_name
        self.st = st
        self.state = state
        self.zip = zip_
    
    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, name, dealership, review, sentiment, purchase, purchase_date=None, car_make=None, car_model=None, car_year=None):
        self.name = name
        self.dealership = dealership
        self.review = review
        self.sentiment = sentiment
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year =  car_year
    
    def __str__(self):
        return "Review: " + self.review