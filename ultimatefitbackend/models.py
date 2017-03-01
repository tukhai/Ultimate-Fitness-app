from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

class MenuCategory(models.Model):
    name = models.CharField(max_length=320)
    description = models.TextField()
    image = models.TextField()

    def __str__(self):
        return self.name

class Menu(models.Model):
    name = models.CharField(max_length=320)
    description = models.TextField()
    image = models.TextField()
    menucategory = models.ForeignKey(MenuCategory)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=320)
    address = models.TextField()
    phone = models.TextField()
    history = models.TextField()

    def __str__(self):
        return self.name

class Order(models.Model):
    name = models.CharField(max_length=320)
    price = models.CharField(max_length=320)
    order_date = models.DateTimeField('date published')
    customer = models.ForeignKey(Customer)

    def __str__(self):
        return self.name

class FoodCategory(models.Model):
    name = models.CharField(max_length=320)
    image = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=320)
    description = models.TextField()
    image = models.TextField()
    menu = models.ForeignKey(Menu)
    order = models.ForeignKey(Order)
    foodcategory = models.ForeignKey(FoodCategory)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Foods'
