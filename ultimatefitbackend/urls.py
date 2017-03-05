from django.conf.urls import url

from . import views

app_name = 'ultimatefitbackend'
urlpatterns = [
    # ex: /ultimatefitbackend/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /ultimatefitbackend/
    url(r'^index.html/$', views.IndexView.as_view(), name='index'),
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
]
