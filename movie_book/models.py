from django.db import models
from django.db.models.base import ModelBase
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey, ForeignObject
#from datetime import datetime
# Create your models here.

class Admin(models.Model):
    name = models.CharField(("name"), max_length=50)
    email = models.EmailField(("E-mail id"), max_length=254)
    password = models.CharField(("password"), max_length=50)


    def __str__(self):
        return self.name
    

class Movies(models.Model):
    mname = models.CharField(("movie_name"), max_length=50)
    category = models.CharField(("category"),max_length=50)
    category2 =models.CharField(("category2"), max_length=50)
    rate = models.PositiveIntegerField(("rating"))
    rdate = models.DateField()
    dur = models.TimeField()
    poster = models.ImageField(upload_to='admin/movies_images/') 
    language =  models.CharField(("language"), max_length=50)
    city = models.CharField(("city"), max_length=50,default='')

    def __str__(self):
         return self.mname

class Users(models.Model):
    Name = models.CharField(("User_Name"), max_length=50)
    Email = models.EmailField(("User_Email"), max_length=254)
    city = models.CharField(("User_city"), max_length=50,default="")
    password = models.CharField(("password"), max_length=50)
    contact = models.PositiveIntegerField(("contact"))

    def __str__(self):
        return self.Name

class Theatre(models.Model):
    Name = models.CharField(("Theatre_Name"), max_length=50)
    Email = models.EmailField(("Theatre_Email"), max_length=254)
    password = models.CharField(("password"), max_length=50)
    contact = models.PositiveIntegerField(("contact"))
    total_screen = models.PositiveIntegerField(("Screen_No"))
    city = models.CharField(("Theatre_city"), max_length=50)

    def __str__(self):
        return self.Name

class Show_available(models.Model):
    movie = models.ForeignKey('Movies',on_delete=models.CASCADE)
    Name = models.ForeignKey('Theatre',on_delete=models.CASCADE)
    date = models.DateField(("Date"), auto_now=False, auto_now_add=False)
    time = models.TimeField(("Time"), auto_now=False, auto_now_add=False)
    screen = models.PositiveIntegerField(("Screen"))
    price = models.PositiveIntegerField(("Price"))

    def __str__(self):
        return self.Name.Name

class Payment(models.Model):
    user = models.ForeignKey('Users',on_delete=models.CASCADE)
    show = models.ForeignKey('Show_available',on_delete=models.CASCADE)
    seat = models.CharField(("seat"), max_length=50)
    ticket = models.PositiveIntegerField(("No Ticket"))
    total = models.PositiveIntegerField(("Total"))

    def __str__(self):
        return self.user.Name
        