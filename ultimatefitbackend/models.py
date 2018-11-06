from __future__ import unicode_literals

import datetime
from time import strftime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

from django.db.models.signals import pre_save
from django.db.models.signals import post_save

from multiselectfield import MultiSelectField

from django.utils.translation import ugettext_lazy as _

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.

class GeneralPromotion(models.Model):
    name = models.CharField(max_length=500)
    percentage = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    startDate = models.DateField("Start Date", unique="true")
    endDate = models.DateField("End Date")

    # def save(self, *args, **kwargs):
    #     try:
    #         GeneralPromotion.objects.get(Q(startDate__range=(self.startDate,self.endDate))|Q(endDate__range=(self.sartDate,self.endDate))|Q(startDate__lt=self.startDate,endDate__gt=self.endDate))
    #         #raise some save error
    #     except GeneralPromotion.DoesNotExist:
    #         super(GeneralPromotion,self).save(*args,**kwargs)

class CouponPromotion(models.Model):
    name = models.CharField(max_length=500)
    coupon_code = models.CharField(max_length=10, unique="true")
    startDate = models.DateField("Start Date")
    endDate = models.DateField("End Date")

    ALL_CATEGORIES = (
        ('PERCENTAGE', 'Percentage (x%)'),
        ('PERCENTAGEWITHCAP', 'Percentage with cap (x%, capped at $y)'),
        ('ABSOLUTEWITHMIN', 'Absolute with min ($x, min $y)'),
    )
    available_categories = MultiSelectField(choices=ALL_CATEGORIES, max_choices=1)

    percentage = models.FloatField("Percentage (%)", null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    percentage_with_cap = models.FloatField("Percentage with cap (%)", null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    cap_percentage = models.IntegerField("Cap percentage ($)", null=True, blank=True)
    absolute_with_min = models.IntegerField("Absolute with min ($)", null=True, blank=True)
    min_absolute = models.IntegerField("Min absolute ($)", null=True, blank=True)

class MenuCategory(models.Model):
    name = models.CharField(max_length=320)
    description = models.TextField()
    image = models.TextField()

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
    name = models.CharField(max_length=320, null=True, blank=True)
    #active = models.BooleanField(max_length=320, null=True, blank=True)
    order_date = models.DateTimeField('date published', null=True, blank=True)
    customer = models.ForeignKey(Customer)
    payment_type = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class FoodCategory(models.Model):
    name = models.CharField(max_length=320)
    image = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name

class FoodType(models.Model):
    name = models.CharField(max_length=320, unique=True, help_text=_('This is the help text'))
    name_vn = models.CharField(max_length=320, null=True, blank=True)
    #description = models.TextField()
    image = models.TextField(null=True, blank=True)
    #price = models.IntegerField(default=0)
    price_lean = models.IntegerField(null=True, blank=True, default=0)
    cal_lean = models.IntegerField(null=True, blank=True, default=0)
    protein_lean = models.IntegerField(null=True, blank=True, default=0)
    carb_lean = models.IntegerField(null=True, blank=True, default=0)
    fat_lean = models.IntegerField(null=True, blank=True, default=0)
    price_maintain = models.IntegerField(null=True, blank=True, default=0)
    cal_maintain = models.IntegerField(null=True, blank=True, default=0)
    protein_maintain = models.IntegerField(null=True, blank=True, default=0)
    carb_maintain = models.IntegerField(null=True, blank=True, default=0)
    fat_maintain = models.IntegerField(null=True, blank=True, default=0)
    price_heavy = models.IntegerField(null=True, blank=True, default=0)
    cal_heavy = models.IntegerField(null=True, blank=True, default=0)
    protein_heavy = models.IntegerField(null=True, blank=True, default=0)
    carb_heavy = models.IntegerField(null=True, blank=True, default=0)
    fat_heavy = models.IntegerField(null=True, blank=True, default=0)
    discount_price = models.IntegerField(null=True, blank=True, default=0)
    LEAN = 'LEAN'
    MAINTAIN = 'MAINTAIN'
    HEAVY = 'HEAVY'
    ALL_CATEGORIES = (
        (LEAN, 'Lean On Me'),
        (MAINTAIN, 'Maintain'),
        (HEAVY, 'Heavy Duty'),
    )
    '''available_categories = models.CharField(
        max_length=2,
        choices=AVAILABLE_CATEGORIES,
        default=MAINTAIN,
    )'''
    # NOT set blank=True means have to have at least 1 choice
    available_categories = MultiSelectField(choices=ALL_CATEGORIES)

    def __str__(self):
        return self.name

class GroupPromotion(models.Model):
    name = models.CharField(max_length=500)
    percentage = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    startDate = models.DateField("Start Date")
    endDate = models.DateField("End Date")
    # food_type = models.ManyToManyField(FoodType, through='GroupPromotionFoodTypes', null=True, blank=True)


class GroupPromotionFoodTypes(models.Model):
    group_promotion = models.ForeignKey(GroupPromotion)
    food_type = models.ForeignKey(FoodType)

    class Meta:
        unique_together = ('group_promotion', 'food_type',)

    def validate_unique(self, *args, **kwargs):
        all_group_promo_food_types = GroupPromotionFoodTypes.objects.all()
        for each_item in all_group_promo_food_types:
            if (each_item.food_type.name == self.food_type.name and each_item.id != self.id):
                StartDate1 = each_item.group_promotion.startDate
                EndDate1 = each_item.group_promotion.endDate
                StartDate2 = self.group_promotion.startDate
                EndDate2 = self.group_promotion.endDate

                if (((StartDate1 <= EndDate2) and (EndDate1 >= StartDate2)) or ((StartDate2 <= EndDate1) and (EndDate2 >= StartDate1))):
                    # print "______________________"
                    # print "OVERLAP", each_item.food_type.name, self.food_type.name
                    raise ValidationError(self.food_type.name + ' has already been discounted on that period')


class Menu(models.Model):
    name = models.CharField(max_length=320)
    description = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    #food_item = models.OneToOneField(FoodItem, null=True, blank=True)
    #food_item = models.Field(FoodItem, null=True, blank=True)
    #ordered_meal = models.OneToManyField(OrderedMeal, blank=True)
    pub_date = models.DateTimeField('date published', null=True, blank=True)
    #menucategory = models.ForeignKey(MenuCategory, null=True, blank=True)
    food_type = models.ManyToManyField(FoodType, through='Food', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['pub_date']

    @property
    def convertdate(self):
        pub_date_string = self.pub_date.date().strftime('%Y-%m-%d')
        return pub_date_string

class Food(models.Model):
    #pub_date = models.DateTimeField('date published', null=True, blank=True)
    #date = pub_date.date()
    #pub_date_string = models.CharField(max_length=320, null=True, blank=True)
    #pub_date_string = date.strftime('%Y-%m-%dT%H:%M')

    order = models.ForeignKey(Order, null=True, blank=True)
    foodcategory = models.ForeignKey(FoodCategory, null=True, blank=True)

    food_type = models.ForeignKey(FoodType, null=True, blank=True)

    LEAN = 'LEAN'
    MAINTAIN = 'MAINTAIN'
    HEAVY = 'HEAVY'
    ALL_CATEGORIES = (
        (LEAN, 'Lean On Me'),
        (MAINTAIN, 'Maintain'),
        (HEAVY, 'Heavy Duty'),
    )
    category = models.CharField(choices=ALL_CATEGORIES, blank=True, max_length=100)
    menu = models.ForeignKey(Menu, null=True, blank=True)
    stock = models.IntegerField(default=0)


    def __str__(self):
        return self.food_type.name

    class Meta:
        verbose_name_plural = 'foods'
        ordering = ['menu']

    def dump(self):
        return {"foodlist":{'name':self.name,
                        'pub_date':self.pub_date,          
                        'description':self.description,
                        'image':self.image,
                        'menu':self.menu.pk,
                        'order':self.order.pk,
                        'foodcategory':self.foodcategory.pk}}

    #def create_food_object_of_all_type(sender, instance, **kwargs):

    @staticmethod
    def post_save(sender, instance, **kwargs):
        #print instance
        #print instance.food_type.available_categories.__len__()
        for i in range(instance.food_type.available_categories.__len__()):
            #print i, instance.food_type.available_categories[i]
            food = Food(food_type=instance.food_type, category=instance.food_type.available_categories[i], menu=instance.menu)
            post_save.disconnect(Food.post_save, Food)
            food.save()
            post_save.connect(Food.post_save, Food)
        instance.delete()

    @property
    def convertdate_from_menu(self):
        pub_date_string = self.menu.convertdate
        return pub_date_string

    @property
    def price_from_foodtype(self):
        if self.category == 'LEAN':
            return self.food_type.price_lean
        elif self.category == 'MAINTAIN':
            return self.food_type.price_maintain
        elif self.category == 'HEAVY':
            return self.food_type.price_heavy

    @property
    def cal_from_foodtype(self):
        if self.category == 'LEAN':
            return self.food_type.cal_lean
        elif self.category == 'MAINTAIN':
            return self.food_type.cal_maintain
        elif self.category == 'HEAVY':
            return self.food_type.cal_heavy

    @property
    def protein_from_foodtype(self):
        if self.category == 'LEAN':
            return self.food_type.protein_lean
        elif self.category == 'MAINTAIN':
            return self.food_type.protein_maintain
        elif self.category == 'HEAVY':
            return self.food_type.protein_heavy

    @property
    def carb_from_foodtype(self):
        if self.category == 'LEAN':
            return self.food_type.carb_lean
        elif self.category == 'MAINTAIN':
            return self.food_type.carb_maintain
        elif self.category == 'HEAVY':
            return self.food_type.carb_heavy

    @property
    def fat_from_foodtype(self):
        if self.category == 'LEAN':
            return self.food_type.fat_lean
        elif self.category == 'MAINTAIN':
            return self.food_type.fat_maintain
        elif self.category == 'HEAVY':
            return self.food_type.fat_heavy

post_save.connect(Food.post_save, Food)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    # user = models.OneToOneField(User, blank=True, null=True, related_name='cart')
    active = models.BooleanField(default=True)
    order_date = models.DateField(null=True)
    payment_type = models.CharField(max_length=100, null=True)
    payment_id = models.CharField(max_length=100, null=True)
    # session_key = models.CharField(max_length=40, null=True, blank=True)

    '''class Meta:
        unique_together = ('user', 'session_key',)'''

    def add_to_cart(self, food_id):
        food = Food.objects.get(pk=food_id)
        try:
            preexisting_order = FoodOrder.objects.get(food=food, cart=self)
            preexisting_order.quantity += 1
            preexisting_order.save()
        except FoodOrder.DoesNotExist:
            new_order = FoodOrder.objects.create(
                food=food,
                cart=self,
                quantity=1
            )
            new_order.save()

    def remove_from_cart(self, food_id):
        food = Food.objects.get(pk=food_id)
        try:
            preexisting_order = FoodOrder.objects.get(food=food, cart=self)
            if preexisting_order.quantity > 1:
                preexisting_order.quantity -= 1
                preexisting_order.save()
            else:
                preexisting_order.delete()
        except FoodOrder.DoesNotExist:
            pass

    def remove_all_from_cart(self, food_id):
        food = Food.objects.get(pk=food_id)
        try:
            preexisting_order = FoodOrder.objects.get(food=food, cart=self)
            preexisting_order.delete()
        except FoodOrder.DoesNotExist:
            pass

    def dump(self):
        return {"cart":{'user':self.user.pk,
                        'order_date':self.order_date,          
                        'payment_type':self.payment_type,
                        'payment_id':payment_id}}


class FoodOrder(models.Model):
    food = models.ForeignKey(Food)
    cart = models.ForeignKey(Cart)
    quantity = models.IntegerField()


class DeliveryOrder(models.Model):
    # order_data = models.OneToOneField(
    #     FoodOrder,
    #     # on_delete=models.CASCADE,
    #     primary_key=True
    # )
    # order_data = models.ForeignKey(FoodOrder, null=True, blank=True)
    order_data = models.TextField(null=True, blank=True)
    order_date = models.DateTimeField(null=True)
    user = models.ForeignKey(User, null=True, blank=True)
    address_info = models.TextField(null=True, blank=True)


class AddressBook(models.Model):
    country = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, null=True, blank=True)
