from django.conf.urls import url, include

from . import views

app_name = 'ultimatefitbackend'
urlpatterns = [
    # ex: /ultimatefitbackend/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /ultimatefitbackend/
    url(r'^base.html/$', views.IndexView.as_view(), name='index'),
    # ex: /ultimatefitbackend/5/
    url(r'^contact.html/$', views.ContactView.as_view(), name='contact'),
    # ex: /ultimatefitbackend/5/
    url(r'^about-us.html/$', views.AboutView.as_view(), name='about'),
    # ex: /ultimatefitbackend/5/
    url(r'^Testimonials.html/$', views.TestimonialsView.as_view(), name='testimonials'),
    # ex: /ultimatefitbackend/5/
    url(r'^404.html/$', views.ErrorView.as_view(), name='404'),
    # ex: /ultimatefitbackend/5/
    url(r'^faq.html/$', views.faqView.as_view(), name='faq'),
    # ex: /ultimatefitbackend/5/
    url(r'^shop.html/$', views.ShopView.as_view(), name='shop'),
    # ex: /ultimatefitbackend/5/
    url(r'^shop-single.html/$', views.ShopsingleView.as_view(), name='shopsingle'),
    # ex: /ultimatefitbackend/5/
    url(r'^foods-list/$', views.foods_list, name='foods_list'),
    # ex: /ultimatefitbackend/5/
    # url(r'food/(?P<name>[\w]+)$', views.food, name='food'),
    url(r'food/(?P<id>[0-9]+)$', views.food, name='food'),
    # URL FOR ADD TO CART
    url(r'^add/(\d+)', views.add, name='add'),  
    #url(r'^remove/(\d+)', views.remove_from_cart, name='remove_from_cart'),
    #url(r'^cart/', views.cart, name='cart'),
    #url(r'^shopping-cart/', include('shopping.urls')),
]
