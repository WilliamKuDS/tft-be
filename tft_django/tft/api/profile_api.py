from django.http import HttpResponse
import tft.service.profile_service as service


def createUpdateProfile(request):
    puuid, region = request.headers['puuid'], request.headers['region']
    data = service.createUpdateProfile(puuid, region)
    return HttpResponse(data)
