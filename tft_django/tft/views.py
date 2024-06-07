from django.shortcuts import render
# from .misc import saveJSONToDatabase
import json
# Create your api here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.forms.models import model_to_dict


def index(request):
    return HttpResponse("You're at the tft_django API. If you are here, you don't know what you are doing.")




