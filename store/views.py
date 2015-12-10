from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from services import create_or_get_store, get_apigee_token
from django.shortcuts import render
import json
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from models import Products, Store

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
            return HttpResponseRedirect("/admin/store/store/%s/change/" % store_created)

class DisplayStoreView(View):
    @csrf_exempt
    def get(self, request):
        context_dict = {}
        store_id = 7
        store_obj = Store.objects.get(id=store_id)
        context_dict['store_data'] = store_obj
        prod_obj = Products.objects.filter(store=store_obj)
        for prod in prod_obj:
            if prod.display_image:
                image_file = prod.display_image.url.split('/')[-1]
                prod.display_image = '/static/' + image_file
        context_dict['product_data'] = prod_obj

        context_dict['product_len'] = prod_obj.count()
        return TemplateResponse(request, 'store.html', context_dict)
