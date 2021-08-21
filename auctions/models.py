from typing import List
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils import timezone

class User(AbstractUser):
    pass
class Category(models.Model):
    category_name=models.CharField(max_length=64)

    def __str__(self) :
        return self.category_name

class Listing(models.Model):
    name=models.CharField(max_length=200)
    description=models.CharField(max_length=600 , default="")
    listed_by=models.ForeignKey(User,on_delete=CASCADE,related_name="listedby")
    category=models.ForeignKey(Category,on_delete=SET_NULL,null=True,default="")
    current_bid=models.FloatField()
    image_url=models.URLField()
    closed = models.BooleanField(default=False)
    def __str__(self) :
        return self.name
    

class Bids(models.Model):
    bid_by=models.ForeignKey(User,on_delete=CASCADE,related_name="bidby")
    listing=models.ForeignKey(Listing,on_delete=CASCADE,related_name="bidon")
    bid = models.FloatField()
    def __str__(self):
        return f"{self.bid} by {self.bid_by} on {self.listing}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ManyToManyField(Listing,blank=True,related_name='watchlist_item',null=True)

    def __str__(self) :
        return f"{self.user}'s wishlist"


class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_who_make_the_comment')
    comment = models.TextField(default="")
    listing=models.ForeignKey(Listing,on_delete=CASCADE,)
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return '%s %s' % (self.user, self.date)