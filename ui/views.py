from django.shortcuts import render
from django.http import HttpResponse
from smashgames.models import Match

# Create your views here.
def index(request):
    return render(request, 'ui/index.html')

def submit_youtube_link(request):
    url = request.POST.get('url', None)
    if url:
        # Check for duplicate
        if Match.objects.filter(video_url=url).count() > 0:
            return HttpResponse("This is a duplicate.")
        else:
            # Create a match 
            return HttpResponse("I got your thing!")
    # url field didn't exist!
    else:
        return HttpResponse("LOL")
    return HttpResponse(request.POST['url'])

def update(request):
    return render(request, 'ui/update.html')
