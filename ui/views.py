from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
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
        return HttpResponse("Something went wrong")
    return HttpResponse(request.POST['url'])

def link_details(request, video_id):
    try:
        VideoURL.objects.get(pk=video_id)
    except:
        return HttpResponseNotFound("Seems like this don't exist?")
    return render(request, 'ui/link-details.html')

def update(request):
    return render(request, 'ui/update.html')

def populate(request):
    from smashconstants.models import GameTitle, Character

    # Populate game constants:
    melee_characters = [
                    'Bowser', 
                    'Captain Falcon', 
                    'Donkey Kong', 
                    'Dr. Mario',
                    'Falco',
                    'Fox',
                    'Ganondorf',
                    'Ice Climbers',
                    'Jigglypuff',
                    'Kirby',
                    'Link',
                    'Luigi',
                    'Mario',
                    'Marth'
                    'Mewtwo',
                    'Mr. Game & Watch',
                    'Ness',
                    'Peach',
                    'Pichu',
                    'Pickachu',
                    'Roy',
                    'Samus',
                    'Shiek',
                    'Yoshi',
                    'Young Link',
                    'Zelda',
                    'Zelda-Shiek']
    brawl_characters = [
                    'Bowser', 
                    'Captain Falcon', 
                    'Charizard',
                    'Diddy Kong',
                    'Donkey Kong',
                    'Falco',
                    'Fox',
                    'Ganondorf',
                    'Ice Climbers',
                    'Ike',
                    'Ivysaur',
                    'Jigglypuff',
                    'King Dedede',
                    'Kirby',
                    'Link',
                    'Lucario',
                    'Lucas',
                    'Luigi',
                    'Mario',
                    'Marth'
                    'Mr. Game & Watch',
                    'Ness',
                    'Olimar',
                    'Peach',
                    'Pickachu',
                    'Pit',
                    'Pokemon Trainer',
                    'R.O.B.',
                    'Samus',
                    'Shiek',
                    'Snake',
                    'Sonic',
                    'Squirtle',
                    'Toon Link',
                    'Wario',
                    'Wolf',
                    'Yoshi',
                    'Zelda',
                    'Zelda-Shiek',
                    'Zero Suit Samus']
    players = [
               'Mango', 
               'Mew2King', 
               'Hungrybox', 
               'Wobbles', 
               'Shroomed']

    try:
        melee = GameTitle(name='Melee')
        melee.save()
        brawl = GameTitle(name='Brawl')
        brawl.save()
    except:
        melee = GameTitle.objects.get(name='Melee')
        brawl = GameTitle.objects.get(name='Brawl')

    for game in [melee, brawl]:
        character_list = {
                        melee: melee_characters, 
                        brawl: brawl_characters}
        for character_name in character_list[game]:
            try:
                character = Character.objects.get(name=character_name)
            except:
                character = Character(name=character_name)
            character.save()
            character.games.add(game)
            character.save()

    return HttpResponse("Okay!")