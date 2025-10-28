from django.db import models
from django.contrib.auth.models import AbstractUser
from .mdate import todaydate

# Create your models here.
class users(AbstractUser):
    username=models.CharField(max_length=52,primary_key=True)
    firstname=models.CharField(max_length=52)
    lastname=models.CharField(max_length=52)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=128,default=0000)
    datajoined=models.DateTimeField(auto_now_add=True)
    balance=models.FloatField(default=10000.0)
    stockbuy=models.JSONField(default=dict)
    stocksold=models.JSONField(default=dict)
    watchlist=models.JSONField(default=dict)
    cache=models.JSONField(default=dict)

    def __str__(self):
        return self.username

class transactions(models.Model):
    username = models.ForeignKey(users, on_delete=models.CASCADE)
    stocknames = models.CharField(max_length=25)
    quantity = models.IntegerField()
    action = models.CharField(max_length=7)
    time = models.DateField(default=todaydate)
    price = models.FloatField(max_length=25.00)