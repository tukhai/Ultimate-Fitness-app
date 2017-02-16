from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core import serializers
import math
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *


def index(request):
    template = loader.get_template('index.html')
    context = {
        'categories': Category.objects.all(),
    }
    return HttpResponse(template.render(context, request))


def exercise(request, id):
    template = loader.get_template('exercise.html')
    context = {
        'exercise': Exercise.objects.get(id=id)
    }
    return HttpResponse(template.render(context, request))

def categories_list(request):
    response_data = serializers.serialize('python',Category.objects.all())
    return JsonResponse(response_data, safe=False)

def exercises_list(request,page):
    page = int(page)
    numObject = Exercise.objects.count()
    numPage = math.ceil(numObject/10)

    exercise_list = Exercise.objects.all()
    paginator = Paginator(exercise_list, 10)  # Show 25 contacts per page

    # page = request.GET.get('page')
    try:
        exercises = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        exercises = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        exercises = paginator.page(paginator.num_pages)

    data = {'obj1': [o.dump() for o in exercises], 'page': paginator.num_pages}
    jsonResult = json.dumps(data)

    return HttpResponse(jsonResult)


