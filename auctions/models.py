from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    imageUrl = models.CharField(max_length=64)
    startBid = models.FloatField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    active = models.BooleanField(default=True)
    timestamp = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    content = models.CharField(max_length=1000)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    timestamp = models.DateField(default=datetime.date.today)

class Category(models.Model):
    name = models.CharField(max_length=24)
    listings = models.ManyToManyField(Listing, blank=True, related_name="categories")

    def __str__(self):
        return f"{self.name}"
    
class Watchlist(models.Model):
    listings = models.ManyToManyField(Listing, blank=True, related_name="watchlists")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")

class Bid(models.Model):
    amount = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.amount}"


