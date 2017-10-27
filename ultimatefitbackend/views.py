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

from django.utils.timezone import utc
from django.core.serializers.json import DjangoJSONEncoder

from django.core.urlresolvers import reverse

from django.contrib.sessions.models import Session

from django.core.exceptions import MultipleObjectsReturned

#from carton.cart import Cart

from .models import Food, FoodCategory, Order, Customer, Menu, MenuCategory, FoodOrder, Cart

# from .utcisoformat import utcisoformat

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
    }

    return render(request, 'base.html', context)


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


def shop(request):
    '''count = Book.objects.all().count()
    context = {
        'count': count,
    }'''

    foods = Food.objects.all()
    context_object_name = 'latest_food_list'
    context = {
        'foods': foods,
    }
    
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

    context = {
        'food': Food.objects.get(pk=food_id),
        'quantityInThisCart': quantityInCart
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
            total_ano += (order_ano.food.price * order_ano.quantity)
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
            foodnames_ano.append(order_ano.food.name)
        print 'AAAAAAAA'
        print foodnames_ano
        print 'AAAAAAAA'
        
        foodnames = []
        for order in orders:
            foodnames.append(order.food.name)
        print 'BBBBBBB'
        print foodnames
        print 'BBBBBBB'                

        # Add the quantity to the existing object in user cart
        for order in orders:
            if order.food.name in foodnames_ano:
                order.quantity += order_ano.quantity
                order.save()                

        # When the object exist in anonymous cart, but not in user cart, so have to create the foodorder object first
        for order_ano in orders_ano:
            if not order_ano.food.name in foodnames:
                order = FoodOrder.objects.create(
                    cart = Cart.objects.get(
                        user=request.user.id,
                        active=True
                    ),
                    food = Food.objects.get(name = order_ano.food.name),
                    quantity = order_ano.quantity
                )
                order.save()                        
    
        orders.update() # Just update orders, no need to do the 2nd query
        # Pull data from db again to have the most updated orders
        # orders = FoodOrder.objects.filter(cart=cart)        

        total = 0
        count = 0
        for order in orders:
            total += ((order.food.price * order.quantity) + total_ano) 
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
        request.session.set_expiry(300)

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
        """Return the last five published questions."""
        '''return Question.objects.order_by('-pub_date')[:5]'''

        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Food.objects.filter(
            description__lte=timezone.now()
        ).order_by('description')[:5]


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
    response_data = serializers.serialize('python',Food.objects.all())
    return JsonResponse(response_data, safe=False)
