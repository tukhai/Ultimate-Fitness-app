    else:
        request.session.set_expiry(300)
        '''cart, created = Cart.objects.get_or_create(
            session_key = request.session.session_key,
            defaults = {'user': None}
        )'''

        #request.session['cart'] = cart.id

        '''try:
            #cart = Cart.objects.get(id=request.session['cart'])
        except (KeyError, Cart.DoesNotExist):
            cart = Cart.objects.create(
                session_key = request.session.session_key
            )'''

        '''request.session['cart'] = Cart.objects.filter(
            user=request.user.id,
            active=True
        )'''

        #Try to store Cart object directly into session
        #but meet with error is not JSON serializable
        '''if 'cart' in request.session:
            cart = request.session['cart']
        else:
            request.session['cart'] = serializers.serialize('json',Cart.objects.create())'''

        #Try to store only cart id into session
        #so cart id would be unique for each anonymous user
        '''if not 'cart' in request.session:
            request.session['cart'] = Cart.objects.create(session_key = request.session.session_key)

        cart = request.session['cart']'''

        '''if not 'cart' in request.session:
            cart = Cart.objects.create()
            request.session['cart'] = cart.id

        try:
            cart = Cart.objects.get(id=request.session['cart'])
        except (KeyError, Cart.DoesNotExist):
            cart = None'''

        '''if not 'cart' in request.session:
            print "cart id is not in session"
            cart = Cart.objects.create()
            request.session['cart'] = cart.id

        try:
            cart = Cart.objects.get(id=request.session['cart'])
        except (KeyError, Cart.DoesNotExist):
            cart = None'''


        #x = request.session['cart']
        #print "session key is:"
        #print x

        if 'cart' in request.session:
            print "cart is exist in session"
            cart = Cart.objects.get(id=request.session['cart'])
        else:
            print "cart id is not in session"
            cart = None

        #Try with serializer
        '''#response_data = serializers.serialize('json',Cart.objects.all())

        #Try to store all the cart fields into session
        if not 'cart' in request.session:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
            #request.session['cart'] = Cart.objects.get(id=request.session['cart_id'])

        #request.session['cart'] = serializers.serialize('json',Cart.objects.get(id=request.session['cart_id']))
        request.session['cart'] = serializers.serialize('json',Cart.objects.all())'''
        
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
