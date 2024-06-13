# Create your api here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("You're at the tft_django API. If you are here, you don't know what you are doing.")




