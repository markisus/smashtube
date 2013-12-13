from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from smashgames.models import VideoURL, Tournament, Match, Set
from smashconstants.models import GameTitle
import re
# Create your views here.
def index(request):
    latest = VideoURL.objects.all()
    return render(request, 'ui/index.html', {'latest': latest})

def embedify_youtube_link(link):
    print link
    version_1 = 'youtu\.be/(\w+)'
    version_2 = 'youtube\.com/watch\?v=(\w+)'
    youtube_id = None
    try:
        youtube_id = re.search(version_1, link).group(1)
        print "Found ytid1!"
    except Exception as e:
        print str(e)
    try:
        youtube_id = re.search(version_2, link).group(1)
        print "Found ytid2!"
    except Exception as e:
        print str(e)

    if not youtube_id:
        raise ValueError("Not a valid youtube link")

    return 'http://youtu.be/' + youtube_id

# Allow for putting a status_code as an argument
def _HttpResponse(*args, **kwargs):
    status_code = kwargs.get('status_code')
    if status_code:
        del kwargs['status_code']
        r = HttpResponse(*args, **kwargs)
        r.status_code = status_code
    else:
        r = HttpResponse(*args, **kwargs)
    return r

def submit_youtube_link(request):
    url = request.POST.get('url', None)
    try:
        url = embedify_youtube_link(url)
    except ValueError as e:
        return _HttpResponse(str(e), status_code=422)
    if url:
        # Check for duplicate
        if VideoURL.objects.filter(video_url=url).count() > 0:
            return HttpResponse("This is a duplicate.")
        else:
            # Store it

            VideoURL(video_url=url).save()
            return HttpResponse("Okay!")
    # url field didn't exist!
    else:
        return _HttpResponse("Something went wrong", status_code=422)
    return HttpResponse(request.POST['url'])

def link_details(request, video_id):
    try:
        video_url = VideoURL.objects.get(pk=video_id)
    except:
        return HttpResponseNotFound("Seems like this don't exist?")
    return render(request, 'ui/link-details.html', {'url': video_url})

def submit_set_for_link(request, link_id):
    video_url_model = VideoURL.objects.get(pk=link_id)

    tournament = request.POST.get('tournament', None)
    game_title = request.POST.get('game-title')
    description = request.POST.get('description', '')
    index = request.POST.get('index', None)
    index = int(index) if index and int(index) > 0 else 1

    if game_title != 'Melee':
        raise Exception("Please say Melee")
    game_title_model = GameTitle.objects.get(name=game_title)
    tournament_model = None
    if tournament:
        try:
            tournament_model = Tournament.objects.get(name=tournament)
        except:
            tournament_model = Tournament(name=tournament)
            tournament_model.save()

    set_model = Set(
        tournament=tournament_model,
        game_title=game_title_model,
        description=description,
        index=index)
    set_model.save()

    match_model = Match(video_url = video_url_model, set=set_model)
    match_model.save()

    return HttpResponse("Okay!")
    

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