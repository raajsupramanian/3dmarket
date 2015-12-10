from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from services import create_or_get_store, get_apigee_token
from django.shortcuts import render
import json

class AuthView(View):
    @csrf_exempt
    def get(self, request):
        token = get_apigee_token()
        if token:
            return HttpResponse(json.dumps({'access_token':token}), content_type="application/json")

class CreateStoreView(View):
    @csrf_exempt
    def post(self, request):
        store_created = create_or_get_store(request)
        if store_created:
            return HttpResponse('correct')

class DisplayStoreView(View):
    @csrf_exempt
    def get(self, request):
        return HttpResponse('correct')

