from django.conf.urls import url, include

from . import views

app_name = 'ultimatefitbackend'
urlpatterns = [
    
    #url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.index, name='index'),
    
    #url(r'^base.html/$', views.IndexView.as_view(), name='index'),
    
    #url(r'^contact.html/$', views.ContactView.as_view(), name='contact'),
    url(r'^contact/', views.contact, name='contact'),
    
    # url(r'^about-us.html/$', views.AboutView.as_view(), name='about'),
    url(r'^about/', views.about, name='about'),
    
    #url(r'^Testimonials.html/$', views.TestimonialsView.as_view(), name='testimonials'),
    url(r'^testimonials/', views.testimonials, name='testimonials'),    
    
    #url(r'^404.html/$', views.ErrorView.as_view(), name='404'),
    url(r'^error/', views.error, name='error'),
    
    #url(r'^faq.html/$', views.faqView.as_view(), name='faq'),
    url(r'^faq/', views.faq, name='faq'),
    
    #url(r'^shop.html/$', views.ShopView.as_view(), name='shop'),
    url(r'^shop/', views.shop, name='shop'),
    
    url(r'^shop-single.html/$', views.ShopsingleView.as_view(), name='shopsingle'),

    url(r'^checkout.html/$', views.CheckoutView.as_view(), name='checkout'),

    url(r'^start_page/$', views.start_page, name='start_page'),

    # URL FOR RETURN JSON
    url(r'^foods-list/$', views.foods_list, name='foods_list'),
    
    url(r'^food/(\d+)', views.food, name='food'),
    # URL FOR ADD TO CART
    url(r'^add/(\d+)', views.add_to_cart, name='add_to_cart'),
    #url(r'^add/[\d+]', views.add_to_cart, name='add_to_cart'),
    url(r'^remove/(\d+)', views.remove_from_cart, name='remove_from_cart'),

    url(r'^removeall/(\d+)', views.remove_all_from_cart, name='remove_all_from_cart'),
    url(r'^cart/', views.cart, name='cart'),

    url(r'^total/', views.total, name='total'),
    url(r'^list/', views.list, name='list'),
    url(r'^registration_validation/', views.registration_validation, name='registration_validation'),
    #url(r'^remove/(\d+)', views.remove_from_cart, name='remove_from_cart'),
    #url(r'^cart/', views.cart, name='cart'),
    #url(r'^shopping-cart/', include('shopping.urls')),
]
