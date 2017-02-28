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
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /ultimatefitbackend/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /ultimatefitbackend/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
