from django.db import models
from django.utils.timezone import now


# Create your models here.


class CarMake(models.Model):
    # Fields
    name = models.CharField(max_length=100)
    description = models.TextField()

    # Methods
    def __str__(self):
        return self.name

class CarModel(models.Model):
    # Fields
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='car_models')
    name = models.CharField(max_length=100)
    dealer_id = models.CharField(max_length=100)  # Assuming it's a string field to store the dealer id
    TYPE_CHOICES = (
            ('Sedan', 'Sedan'),
            ('SUV', 'SUV'),
            ('WAGON', 'WAGON'),
        )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    year = models.DateField()

    # Methods
    def __str__(self):
        return f'{self.dealer_id} {self.make} {self.name} {self.type} {self.year}'


class CarDealer:
    def __init__(self, dealer_id, name, location, contact):
        self.dealer_id = dealer_id
        self.name = name
        self.location = location
        self.contact = contact

    def __str__(self):
        return f"{self.name} - {self.location}"

class DealerReview:
    def __init__(self, review_id, dealer_id, review_text, rating, reviewer_name, review_date):
        self.review_id = review_id
        self.dealer_id = dealer_id
        self.review_text = review_text
        self.rating = rating
        self.reviewer_name = reviewer_name
        self.review_date = review_date

    def __str__(self):
        return f"Review ID: {self.review_id}\n" \
               f"Dealer ID: {self.dealer_id}\n" \
               f"Review Text: {self.review_text}\n" \
               f"Rating: {self.rating}\n" \
               f"Reviewer Name: {self.reviewer_name}\n" \
               f"Review Date: {self.review_date}"