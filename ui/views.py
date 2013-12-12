from django.shortcuts import render
from django.http import HttpResponse
from smashgames.models import VideoURL

# Create your views here.
def index(request):
    latest = VideoURL.objects.all()
    return render(request, 'ui/index.html', {'latest': latest})

def submit_youtube_link(request):
    url = request.POST.get('url', None)
    if url:
        # Check for duplicate
        if VideoURL.objects.filter(video_url=url).count() > 0:
            return HttpResponse("This is a duplicate.")
        else:
            # Store it
            VideoURL(video_url=url).save()
            return HttpResponse("I got your thing!")
    # url field didn't exist!
    else:
        return HttpResponse("LOL")
    return HttpResponse(request.POST['url'])

def link_details(request):
    return HttpResponse("Here is your link details")

def update(request):
    return render(request, 'ui/update.html')
