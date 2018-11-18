from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import loader
from django.views import generic
from django.utils import timezone

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

from django.core import serializers
import math
import json
import time

from time import strftime
import datetime

from django.utils.timezone import utc
from django.core.serializers.json import DjangoJSONEncoder

from django.core.urlresolvers import reverse

from django.contrib.sessions.models import Session

from django.core.exceptions import MultipleObjectsReturned

from django.core.mail import send_mail

#from carton.cart import Cart

from .models import Food, FoodCategory, FoodType, Order, Customer, Menu, MenuCategory, FoodOrder, Cart, GeneralPromotion, GroupPromotion, CouponPromotion, DeliveryOrder, AddressBook

# from .utcisoformat import utcisoformat

from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import activate

from django.db.models import Q

#from django import forms

from .dictionary import dictionary_translation

class IndexView(generic.ListView):
    template_name = 'ultimatefitbackend/base.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        '''return Question.objects.order_by('-pub_date')[:5]'''

        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Food.objects.filter(
            description__lte=timezone.now()
        ).order_by('description')[:5]


def index(request):
    '''if request.user.is_authenticated():
        cart = Cart.objects.get(
            user=request.user,
            active=True
        );
    else:
        if 'cart' in request.session:
            print "cart is exist in session"
            cart = Cart.objects.get(id=request.session['cart'])
        else:
            print "cart id is not in session"
            cart = None

    orders = FoodOrder.objects.filter(cart=cart)
    print orders
    total = 0
    count = 0
    for order in orders:
        total += (order.food.price * order.quantity) 
        count += order.quantity
        print order.food.id,order.food.name,": $",order.food.price," * ",order.quantity

    context = {
        'cart': orders,
        'total': total,
        'count': count,
    }

    return render(request, 'base.html', context)'''

    if request.user.is_authenticated():        

        # Create cart_ano object in session for anonymous use

        # Although this code works, the code arrangement MAY BE not correct logically
        # because all the action for anonymous cart suppose to be only in the case
        # when there's anonymous cart exist in session;
        # For this code, the empty cart_ano in the case when no anonymous cart in
        # session would still be added, minus, etc

        # However, to a certain extend, the logical still ok

        # We would TRY to arrange this code to be logically better, but it's not too important
        # if the code run ok
        if 'cart' in request.session:
            print "cart is exist in session"
            print request.session            
            cart_ano = Cart.objects.get(id=request.session['cart'])
            try:
                cart = Cart.objects.get(
                    user=request.user,
                    active=True
                )
            except ObjectDoesNotExist:
                cart = Cart.objects.create(
                    user=request.user
                )
                cart.save()
            print 'finish create new cart object for user'
            print cart                        
        else:
            print "cart id is not in session"
            cart_ano = None
        ###########################################################

        orders_ano = FoodOrder.objects.filter(cart=cart_ano)
        total_ano = 0
        count_ano = 0
        for order_ano in orders_ano:
            total_ano += (order_ano.food.price_from_foodtype * order_ano.quantity)
            count_ano += order_ano.quantity
        print 'count_ano is: '
        print count_ano
        print 'End'

        cart = Cart.objects.filter(
            user=request.user.id,
            active=True
        )        

        orders = FoodOrder.objects.filter(cart=cart)
        print 'orders 1 are ...'
        print orders        

        foodnames_ano = []
        for order_ano in orders_ano:
            foodnames_ano.append(order_ano.food.food_type.name)
        print 'AAAAAAAA'
        print foodnames_ano
        print 'AAAAAAAA'
        
        foodnames = []
        for order in orders:
            foodnames.append(order.food.food_type.name)
        print 'BBBBBBB'
        print foodnames
        print 'BBBBBBB'                

        # Add the quantity to the existing object in user cart
        for order in orders:
            if order.food.food_type.name in foodnames_ano:
                order.quantity += order_ano.quantity
                order.save()                

        # When the object exist in anonymous cart, but not in user cart, so have to create the foodorder object first
        for order_ano in orders_ano:
            if not order_ano.food.food_type.name in foodnames:
                order = FoodOrder.objects.create(
                    cart = Cart.objects.get(
                        user=request.user.id,
                        active=True
                    ),
                    food = Food.objects.get(name = order_ano.food.food_type.name),
                    quantity = order_ano.quantity
                )
                order.save()                        
    
        orders.update() # Just update orders, no need to do the 2nd query
        # Pull data from db again to have the most updated orders
        # orders = FoodOrder.objects.filter(cart=cart)        

        total = 0
        count = 0
        for order in orders:
            total += ((order.food.price_from_foodtype * order.quantity) + total_ano) 
            count += (order.quantity + count_ano)
        print 'orders 2 are ...'
        print orders
        context = {
            'cart': orders,
            'total': total,
            'count': count,
        }

        # When logged in and go to cart page, after add anonymous cart into user's cart,
        # we should delete the redundant anonymous cart in the db and the cart id in session
        if 'cart' in request.session:

            print 'anonymous cart id is:'
            print request.session['cart']

            # delete the anonymous cart in the db based on the cart.id value saved in session
            Cart.objects.filter(id=request.session['cart']).delete()

            # delete the session to free the session, prevent redundant stuff
            del request.session['cart']

        #return render(request, 'base.html', context)
        return render(request, 'ultimatefitbackend/order.html', context)
    
    else:
        #request.session.set_expiry(300)

        # Track previous url        
        previous_url = request.META.get('HTTP_REFERER')
        print "Previous url is: ", previous_url, type(previous_url)


        if 'cart' in request.session:
            print "cart is exist in session"
            cart = Cart.objects.get(id=request.session['cart'])
        else:
            print "cart id is not in session"
            cart = None

        orders = FoodOrder.objects.filter(cart=cart)
        print orders
        total = 0
        count = 0
        for order in orders:
            total += (order.food.price_from_foodtype * order.quantity) 
            count += order.quantity
        context = {
            'cart': orders,
            'total': total,
            'count': count,
            'previous_url': previous_url
        }
        #return render(request, 'base.html', context)
        return render(request, 'ultimatefitbackend/order.html', context)


def meal(request):
    # WHEN THE PAGE IS FRESHLY LOADED, TODAY FOOD WOULD BE QUERIED AND DISPLAYED
    #foods = Food.objects.all()
    '''for food in foods:
        #print food.name, food.convertdate, type(food.convertdate)
        print food.name, food.pub_date.year, type(food.pub_date.year)
    #foods = Food.objects.filter(convertdate="2017-11-08")'''
    # activate('vn')
    # test_foods = FoodType.objects.all()
    # for food_type in test_foods:
    #     print food_type.name, food_type.available_categories, type(food_type.available_categories.__len__())
    #     #dir helps to print all available attributes
    #     #print dir(food_type.available_categories)
    #     print "TEST", food_type.name
    #     # print instance.__dict__['title_fr']
    #     for item in food_type.available_categories:
    #         print item, type(item)

    test_food_objects = Food.objects.all()
    for food in test_food_objects:
        print food.food_type.name, "price: ", food.price_from_foodtype, food.convertdate_from_menu, "categories: ", food.category     
        #print "item: ", item, type(item)

    today = datetime.date.today()
    menu = Menu.objects.filter(pub_date__year=today.year,
                                pub_date__month=today.month,
                                pub_date__day=today.day)
    '''try:
        foods = menu[0].food.all()
    except IndexError:
        foods =  Food.objects.none()'''

    try:
        foods = Food.objects.filter(menu=menu[0])
    except IndexError:
        foods =  Food.objects.none()

    '''foods = Food.objects.filter(pub_date__year=today.year,
                                pub_date__month=today.month,
                                pub_date__day=today.day)'''
    lean_count = foods.filter(category="LEAN").count()
    maintain_count = foods.filter(category="MAINTAIN").count()
    heavy_count = foods.filter(category="HEAVY").count()
    print "lean_count, maintain_count, heavy_count", foods.count()
    context_object_name = 'latest_food_list'

    if request.user.is_authenticated():
        cart = Cart.objects.get(
            user=request.user,
            active=True
        );
    else:
        if 'cart' in request.session:
            print "cart is exist in session"
            cart = Cart.objects.get(id=request.session['cart'])
        else:
            print "cart id is not in session"
            cart = None

    orders = FoodOrder.objects.filter(cart=cart)
    print orders
    total = 0
    count = 0
    for order in orders:
        total += (order.food.price_from_foodtype * order.quantity) 
        count += order.quantity
        print order.food.id,order.food.food_type.name,": $",order.food.price_from_foodtype," * ",order.quantity

    '''menu = Menu.objects.all()
    print menu[0], type(menu[0])
    food_item_in_selected_menu = menu[0].food.all()
    print food_item_in_selected_menu[0].name'''

    dict_translation = dictionary_translation()

    context = {
        'cart': orders,
        'total': total,
        'count': count,
        'foods': foods,
        'total_count': foods.count(),
        'lean_count': lean_count,
        'maintain_count': maintain_count,
        'heavy_count': heavy_count,
        'dict_translation': dict_translation
    }
        
    return render(request, 'ultimatefitbackend/meal.html', context)


'''def meal_food_list_update(request):
    # WHEN THE PAGE IS FRESHLY LOADED, TODAY FOOD WOULD BE QUERIED AND DISPLAYED
    #foods = Food.objects.all()
    today = datetime.date.today()
    foods = Food.objects.filter(pub_date__year=today.year,
                                pub_date__month=today.month,
                                pub_date__day=today.day)
    context_object_name = 'latest_food_list'

    if request.user.is_authenticated():
        cart = Cart.objects.get(
            user=request.user,
            active=True
        );
    else:
        if 'cart' in request.session:
            print "cart is exist in session"
            cart = Cart.objects.get(id=request.session['cart'])
        else:
            print "cart id is not in session"
            cart = None

    orders = FoodOrder.objects.filter(cart=cart)
    print orders
    total = 0
    count = 0
    for order in orders:
        total += (order.food.price * order.quantity) 
        count += order.quantity
        print order.food.id,order.food.name,": $",order.food.price," * ",order.quantity

    context = {
        'cart': orders,
        'total': total,
        'count': count,
        'foods': foods
    }
        
    return render(request, 'ultimatefitbackend/meal_food_list_update.html', context)'''


def count_number_of_food(request):
    if request.method == "POST":

        query_date = json.loads(request.POST.get("queryDate"))
        
        menu = Menu.objects.filter(pub_date__year=query_date['queryYear'],
                                pub_date__month=query_date['queryMonth'],
                                pub_date__day=query_date['queryDay'])
        try:
            foods = Food.objects.filter(menu=menu[0])
        except IndexError:
            foods = Food.objects.none()

        lean_count = foods.filter(category="LEAN").count()
        maintain_count = foods.filter(category="MAINTAIN").count()
        heavy_count = foods.filter(category="HEAVY").count()
        print "lean_count, maintain_count, heavy_count", lean_count, maintain_count, heavy_count
    context = {
        'total_count': foods.count(),
        'lean_count': lean_count,
        'maintain_count': maintain_count,
        'heavy_count': heavy_count
    }
        
    return JsonResponse(context, safe=False)
        


def meal_food_list_update_query_by_date(request):
    today = datetime.date.today()

    if request.method == "POST":
        '''query_year = request.POST.get("queryYear","")
        query_month = request.POST.get("queryMonth","")
        query_day = request.POST.get("queryDay","")
        print "get date from front-end: ",query_year, query_month, query_day'''

        query_date = json.loads(request.POST.get("queryDate"))
        #print query_date, type(query_date)
        #print "get date from front-end:",query_date['queryYear'], query_date['queryMonth'], query_date['queryDay']
        
        menu = Menu.objects.filter(pub_date__year=query_date['queryYear'],
                                pub_date__month=query_date['queryMonth'],
                                pub_date__day=query_date['queryDay'])
        try:
            foods = Food.objects.filter(menu=menu[0])
        except IndexError:
            foods = Food.objects.none()

        '''foods = Food.objects.filter(pub_date__year=query_date['queryYear'],
                                    pub_date__month=query_date['queryMonth'],
                                    pub_date__day=query_date['queryDay'])'''
        for food in foods:
            print food.food_type.name
    context_object_name = 'latest_food_list'

    if request.user.is_authenticated():
        cart = Cart.objects.get(
            user=request.user,
            active=True
        );
    else:
        if 'cart' in request.session:
            print "cart is exist in session"
            cart = Cart.objects.get(id=request.session['cart'])
        else:
            print "cart id is not in session"
            cart = None

    orders = FoodOrder.objects.filter(cart=cart)
    print orders
    total = 0
    count = 0
    for order in orders:
        total += (order.food.price_from_foodtype * order.quantity) 
        count += order.quantity
        print order.food.id,order.food.food_type.name,": $",order.food.price_from_foodtype," * ",order.quantity

    dict_translation = dictionary_translation()

    context = {
        'cart': orders,
        'total': total,
        'count': count,
        'foods': foods,
        'dict_translation': dict_translation
    }
        
    return render(request, 'ultimatefitbackend/meal_food_list_update.html', context)


def total(request):
    if request.user.is_authenticated():
        check_authentication = True
        try:
            cart = Cart.objects.get(
                user=request.user,
                active=True
            );
        except ObjectDoesNotExist:
            cart = Cart.objects.create(
                user=request.user
            )
            cart.save()
    else:
        check_authentication = False
        if 'cart' in request.session:
            print "cart is exist in session"
            cart = Cart.objects.get(id=request.session['cart'])
        else:
            print "cart id is not in session"
            cart = None

    orders = FoodOrder.objects.filter(cart=cart)
    print orders
    total = 0
    count = 0

    for order in orders:
        total += (order.food.price_from_foodtype * order.quantity) 
        count += order.quantity

    #seror = serializers.serialize('python',orders); 

    o = {
        'total': total,
        'check_authentication': check_authentication
    }
    return JsonResponse(o, safe=False)


def list(request):
    if request.user.is_authenticated():
        cart = Cart.objects.get(
            user=request.user,
            active=True
        );
    else:
        if 'cart' in request.session:
            print "cart is exist in session"
            cart = Cart.objects.get(id=request.session['cart'])
        else:
            print "cart id is not in session"
            cart = None

    # order_by('food') has helped to order by pub_date in Food
    # 'food__pub_date' is the order by a field pub_date(include time of the day, not only convertdate) of food
    
    orders = FoodOrder.objects.filter(cart=cart).order_by('food__menu__pub_date')        
    
    print orders
    total = 0
    count = 0
    for order in orders:
        total += (order.food.price_from_foodtype * order.quantity) 
        count += order.quantity
        print order.food.id,order.food.food_type.name,": $",order.food.price_from_foodtype," * ",order.quantity

    # Find first of the day food object to display date
    
    '''# This would print i from 0 to 9
    for i in range(0, 10):
        print i'''

    try:
        print "The first earlies food in menu name: ", orders[0].food.food_type.name
        orders[0].is_first_of_day = True
        #print "DDDDDDDDD ", orders[0].is_first_of_day
        for i in range(0, len(orders)-1):
            if orders[i].food.menu.convertdate != orders[i+1].food.menu.convertdate:
                orders[i+1].is_first_of_day = True
    except IndexError:
        print "NO ITEM IN ORDERS"

    dict_translation = dictionary_translation()

    context = {
        'cart': orders,
        'total': total,
        'count': count,
        'dict_translation': dict_translation
    }

    return render(request, 'ultimatefitbackend/list.html', context)


def registration_validation(request):
    if request.user.is_authenticated():
        print "Have to log out first to register a new account"
        return redirect('/accounts/logout/')
    else:
        if request.method == "POST":
            registration_username = request.POST.get("name","")
            print "input registration name is: ", registration_username
            username_list = []
            users_list = User.objects.all()
            for user in users_list:
                print user.username
                username_list.append(user.username)
            if registration_username in username_list:
                print "The name: ", registration_username, " has already been taken"
                registration_validator = False
            else:
                print "Valid username"
                registration_validator = True

            e = {
                'registration_validator': registration_validator
            }
            return JsonResponse(e, safe=False)
        return redirect('/')


def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else: #Over midnight
        return nowTime >= startTime or nowTime <= endTime


def coupon_code_validation(request):
    if request.method == "POST":
        coupon_code_from_client = request.POST.get("couponCode","")
        
        all_coupon_objects = CouponPromotion.objects.all()

        returnedObj = {
            'coupon_validator': False
        }
        for coupon_object in all_coupon_objects:
            if coupon_code_from_client == coupon_object.coupon_code and isNowInTimePeriod(coupon_object.startDate, coupon_object.endDate, datetime.date.today()):
                returnedObj = {
                    'coupon_validator': True,
                    'coupon_code': coupon_object.coupon_code,
                    'name': coupon_object.name,
                    'type': coupon_object.available_categories[0]
                }
                if coupon_object.available_categories[0] == "PERCENTAGE":
                    returnedObj['percentage'] = coupon_object.percentage
                elif coupon_object.available_categories[0] == "PERCENTAGEWITHCAP":
                    returnedObj['percentage_with_cap'] = coupon_object.percentage_with_cap
                    returnedObj['cap_percentage'] = coupon_object.cap_percentage
                elif coupon_object.available_categories[0] == "ABSOLUTEWITHMIN":
                    returnedObj['absolute_with_min'] = coupon_object.absolute_with_min
                    returnedObj['min_absolute'] = coupon_object.min_absolute
                break

        e = returnedObj
        return JsonResponse(e, safe=False)
    return redirect('/')


def contact(request):
    return render(request, 'ultimatefitbackend/contact.html')
def about(request):
    return render(request, 'ultimatefitbackend/about-us.html')
def testimonials(request):
    return render(request, 'ultimatefitbackend/Testimonials.html')
def error(request):
    return render(request, 'ultimatefitbackend/404.html')
def faq(request):
    return render(request, 'ultimatefitbackend/faq.html')
def start_page(request):
    return render(request, 'ultimatefitbackend/start_page.html')    


def shop(request):
    '''count = Book.objects.all().count()
    context = {
        'count': count,
    }'''

    foods = Food.objects.all()
    context_object_name = 'latest_food_list'

    menus = Menu.objects.all()

    if request.user.is_authenticated():
        cart = Cart.objects.get(
            user=request.user,
            active=True
        );
    else:
        if 'cart' in request.session:
            print "cart is exist in session"
            cart = Cart.objects.get(id=request.session['cart'])
        else:
            print "cart id is not in session"
            cart = None

    orders = FoodOrder.objects.filter(cart=cart)
    print orders
    total = 0
    count = 0
    for order in orders:
        total += (order.food.price_from_foodtype * order.quantity) 
        count += order.quantity
        print order.food.id,order.food.food_type.name,": $",order.food.price_from_foodtype," * ",order.quantity

    context = {
        'cart': orders,
        'total': total,
        'count': count,
        'foods': foods,
        'menus': menus
    }

    '''context = {
        'foods': foods,
    }'''
    
    '''if request.user.is_authenticated():
        request.session['location'] = "Earth"
    else:
        request.session['location'] = "unknown" '''
        
    return render(request, 'ultimatefitbackend/shop.html', context)


def food(request, food_id):
    template = loader.get_template('ultimatefitbackend/food.html')
    if request.user.is_authenticated():
        cart = Cart.objects.get(
            user=request.user,
            active=True
        );
        orders = FoodOrder.objects.filter(cart=cart, food=food_id)
        try:
            quantityInCart = orders[0].quantity
        except IndexError:
            quantityInCart = 0
    else:
        if 'cart' in request.session:
            print "cart is exist in session"
            cart = Cart.objects.get(id=request.session['cart'])
        else:
            print "cart id is not in session"
            cart = None

        # filter to see in this cart, that food of this food_id has what quantity
        orders = FoodOrder.objects.filter(cart=cart, food=food_id)
        print "print quantity of this food in this person's cart"

        # IndexError to catch when orders query set is empty
        try:
            quantityInCart = orders[0].quantity
        except IndexError:
            quantityInCart = 0
        
        print quantityInCart


    # get the current total value of the cart
    orders_total = FoodOrder.objects.filter(cart=cart)
    #print orders
    total = 0
    for order_total in orders_total:
        total += (order_total.food.price_from_foodtype * order_total.quantity)


    context = {
        'food': Food.objects.get(pk=food_id),
        'quantityInThisCart': quantityInCart,
        'total': total
    }
    return HttpResponse(template.render(context, request))


def add_to_cart(request, food_id):

    #session_id = request.session.session_key

    if request.user.is_authenticated():
        try:
            food = Food.objects.get(pk=food_id)
        except ObjectDoesNotExist:
            pass
        else:
            try:
                cart = Cart.objects.get(
                    user=request.user,
                    active=True
                )
            except ObjectDoesNotExist:
                cart = Cart.objects.create(
                    user=request.user
                )
                cart.save()
            cart.add_to_cart(food_id)
        return redirect('ultimatefitbackend:cart')
        #return render(request, 'ultimatefitbackend/shop.html')
    else:
        # return redirect('ultimatefitbackend:index')
        try:
            food = Food.objects.get(pk=food_id)
        except ObjectDoesNotExist:
            pass
        else:
            #request.session.set_expiry(300)

            if 'cart' in request.session:
                print "cart is exist in session"
                print request.session['cart']
                print "END"
                cart = Cart.objects.get(id=request.session['cart'])
            else:
                print "cart id is not in session"
                cart = Cart.objects.create()
                request.session['cart'] = cart.id
                cart.save()
            cart.add_to_cart(food_id)
        return redirect('ultimatefitbackend:cart')        
        #return redirect('ultimatefitbackend:food food.id')        


def remove_from_cart(request, food_id):
    if request.user.is_authenticated():
        try:
            food = Food.objects.get(pk=food_id)
        except ObjectDoesNotExist:
            pass
        else:
            cart = Cart.objects.get(user=request.user, active=True)
            cart.remove_from_cart(food_id)
        return redirect('ultimatefitbackend:cart')
    else:
        # return redirect('ultimatefitbackend:index')
        try:
            food = Food.objects.get(pk=food_id)
        except ObjectDoesNotExist:
            pass
        else:
            #request.session.set_expiry(300)

            if 'cart' in request.session:
                print "cart is exist in session"
                print request.session['cart']
                print "END"
                cart = Cart.objects.get(id=request.session['cart'])
            cart.remove_from_cart(food_id)
        return redirect('ultimatefitbackend:cart')


def remove_all_from_cart(request, food_id):
    if request.user.is_authenticated():
        try:
            food = Food.objects.get(pk=food_id)
        except ObjectDoesNotExist:
            pass
        else:
            cart = Cart.objects.get(user=request.user, active=True)
            cart.remove_all_from_cart(food_id)
        return redirect('ultimatefitbackend:cart')
    else:
        # return redirect('ultimatefitbackend:index')
        try:
            food = Food.objects.get(pk=food_id)
        except ObjectDoesNotExist:
            pass
        else:
            #request.session.set_expiry(300)

            if 'cart' in request.session:
                print "cart is exist in session"
                print request.session['cart']
                print "END"
                cart = Cart.objects.get(id=request.session['cart'])
            cart.remove_all_from_cart(food_id)
        return redirect('ultimatefitbackend:cart')


def cart(request):
    if request.user.is_authenticated():
        # Create cart_ano object in session for anonymous use

        # Although this code works, the code arrangement MAY BE not correct logically
        # because all the action for anonymous cart suppose to be only in the case
        # when there's anonymous cart exist in session;
        # For this code, the empty cart_ano in the case when no anonymous cart in
        # session would still be added, minus, etc

        # However, to a certain extend, the logical still ok

        # We would TRY to arrange this code to be logically better, but it's not too important
        # if the code run ok
        if 'cart' in request.session:
            print "cart is exist in session"
            print request.session            
            cart_ano = Cart.objects.get(id=request.session['cart'])
            try:
                cart = Cart.objects.get(
                    user=request.user,
                    active=True
                )
            except ObjectDoesNotExist:
                cart = Cart.objects.create(
                    user=request.user
                )
                cart.save()
            print 'finish create new cart object for user'
            print cart                        
        else:
            print "cart id is not in session"
            cart_ano = None
        ###########################################################

        orders_ano = FoodOrder.objects.filter(cart=cart_ano)
        total_ano = 0
        count_ano = 0
        for order_ano in orders_ano:
            total_ano += (order_ano.food.price_from_foodtype * order_ano.quantity)
            count_ano += order_ano.quantity
        print 'count_ano is: '
        print count_ano
        print 'End'

        cart = Cart.objects.filter(
            user=request.user.id,
            active=True
        )        

        orders = FoodOrder.objects.filter(cart=cart)
        print 'orders 1 are ...'
        print orders        

        foodnames_ano = []
        for order_ano in orders_ano:
            foodnames_ano.append(order_ano.food.food_type.name)
        print 'AAAAAAAA'
        print foodnames_ano
        print 'AAAAAAAA'
        
        foodnames = []
        for order in orders:
            foodnames.append(order.food.food_type.name)
        print 'BBBBBBB'
        print foodnames
        print 'BBBBBBB'                

        # Add the quantity to the existing object in user cart
        for order in orders:
            if order.food.food_type.name in foodnames_ano:
                order.quantity += order_ano.quantity
                order.save()                

        # When the object exist in anonymous cart, but not in user cart, so have to create the foodorder object first
        for order_ano in orders_ano:
            if not order_ano.food.food_type.name in foodnames:
                order = FoodOrder.objects.create(
                    cart = Cart.objects.get(
                        user=request.user.id,
                        active=True
                    ),
                    food = Food.objects.get(name = order_ano.food.food_type.name),
                    quantity = order_ano.quantity
                )
                order.save()                        
    
        orders.update() # Just update orders, no need to do the 2nd query
        # Pull data from db again to have the most updated orders
        # orders = FoodOrder.objects.filter(cart=cart)        

        total = 0
        count = 0
        for order in orders:
            total += ((order.food.price_from_foodtype * order.quantity) + total_ano) 
            count += (order.quantity + count_ano)
        print 'orders 2 are ...'
        print orders
        context = {
            'cart': orders,
            'total': total,
            'count': count,
        }

        # When logged in and go to cart page, after add anonymous cart into user's cart,
        # we should delete the redundant anonymous cart in the db and the cart id in session
        if 'cart' in request.session:

            print 'anonymous cart id is:'
            print request.session['cart']

            # delete the anonymous cart in the db based on the cart.id value saved in session
            Cart.objects.filter(id=request.session['cart']).delete()

            # delete the session to free the session, prevent redundant stuff
            del request.session['cart']

        return render(request, 'ultimatefitbackend/shop-cart.html', context)
    
    else:
        #request.session.set_expiry(300)

        if 'cart' in request.session:
            print "cart is exist in session"
            cart = Cart.objects.get(id=request.session['cart'])
        else:
            print "cart id is not in session"
            cart = None

        orders = FoodOrder.objects.filter(cart=cart)
        print orders
        total = 0
        count = 0
        for order in orders:
            total += (order.food.price_from_foodtype * order.quantity) 
            count += order.quantity
        context = {
            'cart': orders,
            'total': total,
            'count': count,
        }
        return render(request, 'ultimatefitbackend/shop-cart.html', context)
    

class ShopsingleView(generic.ListView):
    template_name = 'ultimatefitbackend/shop-single.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        '''return Question.objects.order_by('-pub_date')[:5]'''

        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Food.objects.filter(
            description__lte=timezone.now()
        ).order_by('description')[:5]


class CheckoutView(generic.ListView):
    template_name = 'ultimatefitbackend/checkout.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        return Food.objects.all()


def create_order(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            print "posting, create order for checkout.."

            current_cart = Cart.objects.get(user = request.user)
            order_data = FoodOrder.objects.filter(cart = current_cart)

            copied_order_data_arr = []
            for item_order_data in order_data:
                copied_order_data_arr.append({
                    'food_id': item_order_data.food.id,
                    'quantity': item_order_data.quantity
                })

            string_FoodOrder_data_id = json.dumps(copied_order_data_arr)

            # Current date
            order_created_date = datetime.datetime.now()

            delivery_order = DeliveryOrder.objects.create(
                order_data = string_FoodOrder_data_id,
                order_date = order_created_date,
                user = request.user
            )
            delivery_order.save()

            ########### After this have to delete cart ###########
            current_cart.delete()

            ########### Get the id of newly created delivery_order and send to client side ###########
            created_order_ID = delivery_order.id

        return JsonResponse({'created_order_ID': created_order_ID}, safe=False)
    else:
        return redirect('/')


def order(request, created_delivery_id):
    print "request.history", request.META.get('HTTP_REFERER')
    if request.user.is_authenticated() and request.META.get('HTTP_REFERER') != None:

        # Take the latest delivery created, another way is using cookie/session to pass between pages, but this is easier
        # latest_created_delivery = DeliveryOrder.objects.filter(user = request.user).latest('order_date')
        latest_created_delivery = DeliveryOrder.objects.get(id = created_delivery_id)

        order_data_arr = json.loads(latest_created_delivery.order_data)

        rendered_data_arr = []
        total = 0
        count = 0
        number_of_kinds = 0
        for item_arr in order_data_arr:
            food_obj = Food.objects.get(id=item_arr['food_id'])
            print food_obj.food_type.name, item_arr['quantity']
            rendered_data_arr.append({
                'food_obj': food_obj,
                'quantity': item_arr['quantity']
            })

            total += (food_obj.price_from_foodtype * item_arr['quantity']) 
            count += item_arr['quantity']
            number_of_kinds += 1

        context = {
            'delivery_id': created_delivery_id,
            'data_arr': rendered_data_arr,
            'total': total,
            'count': count,
            'number_of_kinds': number_of_kinds
        }

        return render(request, 'ultimatefitbackend/checkout.html', context)
    else:
        return redirect('/')


def order_confirm_email(request, delivery_id):
    if request.user.is_authenticated():
        address_object_from_client = request.POST.get("address_object_data","")
        print address_object_from_client

        delivery_obj_to_be_update = DeliveryOrder.objects.get(id = delivery_id)

        ########### Send order confirmation email ###########
        address_data = json.loads(address_object_from_client)
        msg_content = 'Dear ' + address_data['first_name'] + ' ' + address_data['last_name'] + ',\n' + 'Here is the detail of your order:\n' + address_object_from_client + '\n\nThank you,\nUltimate Fit Team.'

        send_mail(
            'Confirm Your Order',
            msg_content,
            'noreply@ultimate.fit',
            [address_data['email']],
            fail_silently=False,
        )

        # Save address info into Delivery Order table
        delivery_obj_to_be_update.address_info = address_object_from_client
        delivery_obj_to_be_update.save()

        # Save address info into Address Book table
        address_book_item = AddressBook.objects.create(
            country = address_data['country'],
            first_name = address_data['first_name'],
            last_name = address_data['last_name'],
            address = address_data['address'],
            city = address_data['city'],
            email = address_data['email'],
            phone_number = address_data['phone_number'],
            user = request.user
        )
        address_book_item.save()

        return JsonResponse({}, safe=False)
    else:
        # return redirect('/')
        return JsonResponse({}, safe=False)


def success_order(request):
    print request.META.get('HTTP_REFERER')
    if request.user.is_authenticated() and request.META.get('HTTP_REFERER') != None:
        return render(request, 'ultimatefitbackend/success-order.html')
    else:
        return redirect('/')


def account_page(request):
    if request.user.is_authenticated():
        current_user = User.objects.get(id = request.user.id)

        context = {
            'username': current_user.username,
            # 'first_name': current_user.first_name,
            # 'last_name': current_user.last_name,
            'email': current_user.email
        }

        return render(request, 'ultimatefitbackend/account.html', context)
    else:
        return redirect('/')


def account_change_username(request):
    if request.user.is_authenticated():
        new_username_from_client = request.POST.get("new_username","")

        current_user = User.objects.get(id = request.user.id)
        current_user.username = new_username_from_client
        current_user.save()

        return JsonResponse({}, safe=False)
    else:
        return JsonResponse({}, safe=False)


def account_change_email(request):
    if request.user.is_authenticated():
        new_email_from_client = request.POST.get("new_email","")

        current_user = User.objects.get(id = request.user.id)
        current_user.email = new_email_from_client
        current_user.save()
 
        return JsonResponse({}, safe=False)
    else:
        return JsonResponse({}, safe=False)


def account_change_password(request):
    if request.user.is_authenticated():
        current_password_from_client = request.POST.get("current_password","")
        new_password_from_client = request.POST.get("new_password","")

        current_user = User.objects.get(id = request.user.id)

        is_current_password_check_correct = False
        if (current_user.check_password(current_password_from_client)):
            current_user.set_password(new_password_from_client)
            current_user.save()

            is_current_password_check_correct = True

        return JsonResponse({'is_current_password_check_correct': is_current_password_check_correct}, safe=False)
    else:
        return JsonResponse({}, safe=False)


def address_book(request):
    if request.user.is_authenticated():
        address_list = AddressBook.objects.filter(user = request.user)

        context = {
            'address_list': address_list
        }
        return render(request, 'ultimatefitbackend/address-book.html', context)
    else:
        return redirect('/')


def edit_address_book(request):
    if request.user.is_authenticated() and request.method == "POST":
        address_obj_ID_from_client = request.POST.get("address_obj_ID","")
        address_obj_data_from_client = request.POST.get("address_obj_data","")

        address_data = json.loads(address_obj_data_from_client)

        address_obj_to_be_update = AddressBook.objects.get(id = address_obj_ID_from_client)
        ##############
        address_obj_to_be_update.country = address_data['country']
        address_obj_to_be_update.first_name = address_data['first_name']
        address_obj_to_be_update.last_name = address_data['last_name']
        address_obj_to_be_update.address = address_data['address']
        address_obj_to_be_update.city = address_data['city']
        address_obj_to_be_update.email = address_data['email']
        address_obj_to_be_update.phone_number = address_data['phone_number']
        ##############
        address_obj_to_be_update.save()

        return JsonResponse({}, safe=False)
    else:
        return JsonResponse({}, safe=False)


def add_address_book(request):
    if request.user.is_authenticated() and request.method == "POST":

        address_obj_data_from_client = request.POST.get("address_obj_data","")

        address_data = json.loads(address_obj_data_from_client)
        ##############
        address_book_item = AddressBook.objects.create(
            country = address_data['country'],
            first_name = address_data['first_name'],
            last_name = address_data['last_name'],
            address = address_data['address'],
            city = address_data['city'],
            email = address_data['email'],
            phone_number = address_data['phone_number'],
            user = request.user
        )
        address_book_item.save()

        return JsonResponse({}, safe=False)
    else:
        return JsonResponse({}, safe=False)


def delete_address_book(request):
    if request.user.is_authenticated():
        address_obj_ID_from_client = request.POST.get("address_obj_ID","")

        instance_to_be_deleted = AddressBook.objects.get(id=address_obj_ID_from_client)
        instance_to_be_deleted.delete()
        return redirect('ultimatefitbackend:address_book')
    else:
        return redirect('/')


def orders_history(request):
    if request.user.is_authenticated():
        all_orders_of_this_user = DeliveryOrder.objects.filter(user = request.user)

        history_order_arr = []
        for order in all_orders_of_this_user:
            order_data_arr = json.loads(order.order_data)

            rendered_data_arr = []
            total = 0
            count = 0
            number_of_kinds = 0
            for item_arr in order_data_arr:
                food_obj = Food.objects.get(id=item_arr['food_id'])
                rendered_data_arr.append({
                    'food_obj': food_obj,
                    'quantity': item_arr['quantity']
                })

                total += (food_obj.price_from_foodtype * item_arr['quantity']) 
                count += item_arr['quantity']
                number_of_kinds += 1

            history_item = {
                'delivery_id': order.id,
                'date': order.order_date,
                'data_arr': rendered_data_arr,
                'total': total,
                'count': count,
                'number_of_kinds': number_of_kinds
            }

            history_order_arr.append(history_item)

        context = {
            "history_order_arr": history_order_arr 
        }

        return render(request, 'ultimatefitbackend/orders-history.html', context)
    else:
        return redirect('/')


class AccountView(generic.ListView):
    template_name = 'ultimatefitbackend/account.html'
    # context_object_name = 'latest_question_list'
    def get_queryset(self):
        return Food.objects.all()


'''class DetailView(generic.DetailView):
    model = Question
    template_name = 'ultimatefitbackend/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'ultimatefitbackend/results.htm'''


'''def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)
    template = loader.get_template('ultimatefitbackend/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
    # return HttpResponse("Hello, world. You're at the ultimatefitbackend index.")'''

'''def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'ultimatefitbackend/index.html', context)'''

'''def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'ultimatefitbackend/detail.html', {'question': question})'''

'''def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'ultimatefitbackend/detail.html', {'question': question})'''

# Create your views here.

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'ultimatefitbackend/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('ultimatefitbackend:results', args=(question.id,)))


def foods_list(request):
    response_data = serializers.serialize('python', Food.objects.all())
    return JsonResponse(response_data, safe=False)


def general_promotion_list(request):
    response_data = serializers.serialize('python', GeneralPromotion.objects.all())
    return JsonResponse(response_data, safe=False)


def group_promotion_list(request):
    response_data = serializers.serialize('python', GroupPromotion.objects.all())

    group_promotion_list = GroupPromotion.objects.all()
    for item in group_promotion_list:
        print item.name
        for each_food_type in item.food_type.all():
            print each_food_type.name

    return JsonResponse(response_data, safe=False)