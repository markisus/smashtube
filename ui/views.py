from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from smashgames.models import VideoURL, Tournament, Match, Set, Player, PlayerSession
from smashconstants.models import GameTitle
import re

def PreviousPage(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Create your views here.
def index(request):
    # character - character
    # player - character
    # player - player

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

    return 'http://www.youtube.com/embed/' + youtube_id

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
            return _HttpResponse("This is a duplicate.", status_code=422)
        else:
            # Store it

            VideoURL(video_url=url).save()
            return PreviousPage(request)
    # url field didn't exist!
    else:
        return _HttpResponse("Something went wrong", status_code=422)

def link_details(request, video_id):
    try:
        video_url_model = VideoURL.objects.get(pk=video_id)
    except:
        return HttpResponseNotFound("Seems like this don't exist?")

    # Get sets related to this link
    set_models = Set.objects.filter(match__video_url=video_url_model).distinct()
    return render(request, 'ui/link-details.html', {'video_url_model': video_url_model, 'set_models':set_models})

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

    return PreviousPage(request)
 
def delete_set(request):
    set_id = int(request.POST.get('set-id'))
    Set.objects.get(pk=set_id).delete()
    return PreviousPage(request)

def delete_player_session(request):
    PlayerSession.objects.get(pk=int(request.POST.get('player-session-id'))).delete()
    return PreviousPage(request)

def edit_match(request):
    match_model = Match.objects.get(pk=int(request.POST['match-id']))
    match_model.start = request.POST.get('start', '')
    match_model.end = request.POST.get('end', '')
    match_model.index = int(request.POST.get('index', 1)) if int(request.POST.get('index', 1)) > 0 else 1
    match_model.save()
    return PreviousPage(request)

def copy_match(request):
    print "Copying match"
    match_model = Match.objects.get(pk=int(request.POST['match-id']))
    new_index = Match.objects.filter(set=match_model.set).count() + 1
    match_model_copy = Match(set=match_model.set, video_url=match_model.video_url, index=new_index)
    match_model_copy.save()
    player_session_models = match_model.playersession_set.all()
    for player_session_model in player_session_models:
        player_session_model_copy = PlayerSession(player=player_session_model.player,
                      match=match_model_copy,
                      character=player_session_model.character,
                      team=player_session_model.team,
                      index=player_session_model.index)
        player_session_model_copy.save()
    return PreviousPage(request)

def submit_player_for_match(request, match_id):
    match_model = Match.objects.get(pk=int(match_id))
    
    player_name = request.POST['player-name']
    character_name = request.POST['character-name']

    character_model = match_model.set.game_title.character_set.get(name=character_name)

    try:
        player_model = Player.objects.get(name=player_name)
    except:
        player_model = Player(name=player_name)
        player_model.save()

    player_session_model = PlayerSession(
                                         player=player_model, 
                                         match=match_model, 
                                         character=character_model)
    player_session_model.save()
    return PreviousPage(request)
    



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
                    'Marth',
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