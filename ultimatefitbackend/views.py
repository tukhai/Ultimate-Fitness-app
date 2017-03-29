from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import loader
from django.views import generic
from django.utils import timezone

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core import serializers
import math
import json
import time

from time import strftime

from django.utils.timezone import utc
from django.core.serializers.json import DjangoJSONEncoder

from carton.cart import Cart

from .models import Food, FoodCategory, Order, Customer, Menu, MenuCategory

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


class ContactView(generic.ListView):
    template_name = 'ultimatefitbackend/contact.html'
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

class AboutView(generic.ListView):
    template_name = 'ultimatefitbackend/about-us.html'
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

class TestimonialsView(generic.ListView):
    template_name = 'ultimatefitbackend/Testimonials.html'
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

class ErrorView(generic.ListView):
    template_name = 'ultimatefitbackend/404.html'
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

class faqView(generic.ListView):
    template_name = 'ultimatefitbackend/faq.html'
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

class ShopView(generic.ListView):
    model = Food
    template_name = 'ultimatefitbackend/shop.html'
    context_object_name = 'latest_food_list'


    def get_queryset(self):
        """Return the last five published questions."""
        '''return Question.objects.order_by('-pub_date')[:5]'''

        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Food.objects.all()
        #return serializers.serialize('python',Food.objects.all())

def food(request, id):
    template = loader.get_template('ultimatefitbackend/food.html')
    context = {
        'food': Food.objects.get(id=id)
    }
    return HttpResponse(template.render(context, request))


def add(request):
    cart = Cart(request.session)
    food = Food.objects.get(id=request.GET.get('id'))
    cart.add(food, price=food.price)
    return HttpResponse("Added")

def show(request):
    return render(request, 'ultimatefitbackend/show-cart.html')


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
