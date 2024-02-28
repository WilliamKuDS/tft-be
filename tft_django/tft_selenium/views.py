from django.shortcuts import render
from .tft_selenium import tftQuery
from .tft_selenium import getURL
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os

# Create your views here.
@csrf_exempt
def queryUser(request):
    if request.method == 'POST':
        body = json.load(request)
        url = getURL(body['Name'], body['Region'].lower(), body['Tag'])
        player = tftQuery(body['Length'])
        player.getInfo(url)
        return HttpResponse('Got Player!')