from django.http import HttpResponse
from django.shortcuts import render
from tft.models import Game

# Create your views here.
def index(request):
    if request.method == 'GET':
        #data = dp.preprocessData()
        #for i in data:
        #    print(type(i))
        return HttpResponse('test')

