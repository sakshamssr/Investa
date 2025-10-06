from django.db import models
from django.contrib.auth.models import AbstractUser

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