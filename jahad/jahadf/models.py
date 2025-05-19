from django.db import models


class Market(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Item(models.Model):
    brand = models.CharField(max_length=30)
    model = models.TextField()
    price = models.IntegerField()
    market = models.ForeignKey(Market, on_delete=models.CASCADE)

    

class Mobile(Item):
    cname = models.CharField(default='Mobile', max_length=30)

    def __str__(self):
        return self.brand

class Monitor(Item):
    cname = models.CharField(default='Monitor', max_length=30)

    def __str__(self):
        return self.brand

class Laptop(Item):
    cname = models.CharField(default='Laptop', max_length=30)

    def __str__(self):
        return self.brand


# Create your models here.
