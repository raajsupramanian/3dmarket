from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from services import create_or_get_store
from django.shortcuts import render

class CreateStoreView(View):
    @csrf_exempt
    def post(self, request):
        store_created = create_or_get_store(request)
        if store_created:
            return HttpResponse('correct')
