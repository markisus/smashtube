from django.shortcuts import render_to_response
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("OK")

def update(request):
    return render_to_response('ui/update.html')
