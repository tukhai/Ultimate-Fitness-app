# -*- coding: utf-8 -*- 
import os
import json, codecs

from .models import Food, FoodCategory, FoodType, Order, Customer, Menu, MenuCategory, FoodOrder, Cart

PAGES_NEED_CONTEXT_PROCESSOR_CART = [
	"/contact/", 
	"/about/", 
	"/account_page/", 
	"/address_book/", 
	"/orders_history/"
]


def translation_dictionary(request):
	current_directory = os.getcwd()
	with open(current_directory + '/ultimatefitbackend/dict.json') as f:
		data = json.load(f)

	return {
		'dict_translation': data
	}


# render count, total, cart,... globally so all page can have correct cart hover
# try with only total first to see if can solve the problem
def render_total_cart(request):
	if request.path in PAGES_NEED_CONTEXT_PROCESSOR_CART:
		if request.user.is_authenticated():
			if 'cart' in request.session:
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
			else:
				cart_ano = None

			orders_ano = FoodOrder.objects.filter(cart=cart_ano)
			total_ano = 0
			count_ano = 0
			for order_ano in orders_ano:
				total_ano += (order_ano.food.price_from_foodtype * order_ano.quantity)
				count_ano += order_ano.quantity

			cart = Cart.objects.filter(
				user=request.user.id,
				active=True
			)
			orders = FoodOrder.objects.filter(cart=cart)

			foodnames_ano = []
			for order_ano in orders_ano:
				foodnames_ano.append(order_ano.food.food_type.name)
			
			foodnames = []
			for order in orders:
				foodnames.append(order.food.food_type.name)

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
		
			orders.update()

			total = 0
			count = 0
			for order in orders:
				total += ((order.food.price_from_foodtype * order.quantity) + total_ano) 
				count += (order.quantity + count_ano)

			context = {
				'cart': orders,
				'total': total,
				'count': count
			}

			if 'cart' in request.session:
				# delete the anonymous cart in the db based on the cart.id value saved in session
				Cart.objects.filter(id=request.session['cart']).delete()

				# delete the session to free the session, prevent redundant stuff
				del request.session['cart']

			#return render(request, 'base.html', context)
			return context
		else:	   
			previous_url = request.META.get('HTTP_REFERER')

			if 'cart' in request.session:
				cart = Cart.objects.get(id=request.session['cart'])
			else:
				cart = None

			orders = FoodOrder.objects.filter(cart=cart)
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
			return context
	else:
		print "page doesnt need cart obj to be rendered"
		return {}
