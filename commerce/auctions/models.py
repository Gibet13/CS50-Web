from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.enums import Choices


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
   
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    descryption = models.CharField(max_length=240)
    image = models.ImageField(null=True, blank=True, default='',upload_to='img')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    
    opened =models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}, {self.price} €"

class Bid(models.Model):
    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_date = models.DateField(auto_now_add=True)
    value = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.author}, {self.value} € , {self.bid_date}"

class Comment(models.Model):
    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.DateField(auto_now_add=True)
    content = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.author}, {self.comment_date} , {self.content}"

class Watchlist(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listings = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.listings}"

class Winner(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listings = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} won {self.listings}"