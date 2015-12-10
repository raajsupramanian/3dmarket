from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from services import create_or_get_store
from django.shortcuts import render

class CreateStoreView(View):
    @csrf_exempt
    def post(self, request):
        user_obj = create_user(request.POST['email'], request.POST['password'])
        store_name = request.POST['store_name']
        store_id = create_store(user_obj, store_name)
        create_oss_bucket(store_name)

        store_created = create_or_get_store(request)
        if store_created:
            return HttpResponse('correct')


class DisplayStoreView(View):
    @csrf_exempt
    def get(self, request):
        return HttpResponse('correct')


