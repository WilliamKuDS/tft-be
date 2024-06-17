import json
from django.http import HttpResponse
from django.http import JsonResponse
import tft.service.openai_service as service


def analyze_performance(request):
    puuid = request.headers['puuid']
    data = service.analyzePerformance(puuid)
    return JsonResponse(data)


def match_recommendations(request):
    puuid = request.headers['puuid']
    data = service.matchRecommendation(puuid)
    return JsonResponse(data)
