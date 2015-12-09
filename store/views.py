from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

class CreateStoreView(View):
    @csrf_exempt
    def post(self, request):
        return HttpResponse('correct')
