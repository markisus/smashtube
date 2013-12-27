from django.shortcuts import render
import json
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from smashgames.models import VideoURL, Tournament, Match, Set, Player, PlayerSession
from smashconstants.models import Character, GameTitle

@csrf_exempt
def submit_link(request):
    data = json.loads(request.body)
    set_description = data['set_description']
    tournament = data['tournament']
    teams = data['teams']
    link = data['link']
    num_matches = data['num_matches']
    game_title = data['game_title']
    
    # Create tournament
    if tournament:
        try:
            tournament_model = Tournament.objects.get(name=tournament)
        except Tournament.DoesNotExist:
            tournament_model = Tournament(name=tournament)
            tournament_model.save()
    print 'Tournament Okay'
    
    # Create link
    try:
        video_url_model = VideoURL.objects.get(video_url=link)
    except VideoURL.DoesNotExist:
        video_url_model = VideoURL(video_url=link)
        video_url_model.save()
    print 'Link Okay'
        
    # Get Game Title
    game_title_model = GameTitle.objects.get(name=game_title)
    print 'Game Title Okay'
    
    # Create Set
    if tournament:
        set_model = Set(
            tournament=tournament_model, 
            description=set_description, 
            game_title=game_title_model)
    else:
        set_model = Set(
            description=set_description, 
            game_title=game_title_model)
    set_model.save()
    print 'Set Okay'
    
    # Make Matches
    matches = []
    for match_number in range(min(10, num_matches)):
        match_model = Match(set=set_model, index=match_number, video_url=video_url_model)
        match_model.save()
        matches.append(match_model)
    print 'Matches Okay'
    
    # Save Teams
    for team in teams:
        for player_session in team:
            player, character = player_session['player'], player_session['character']
            try:
                player_model = Player.objects.get(name=player)
            except Player.DoesNotExist:
                player_model = Player(name=player)
                player_model.save()
            character_model = Character.objects.get(name=character)
            match_number = 0
            for match in matches:
                player_session_model = PlayerSession(
                    character=character_model,
                    player=player_model, 
                    match=match_model,
                    team=PlayerSession.TEAMS[match_number][0])
                player_session_model.save()
                match_number += 1
    print 'Teams Okay'
    
    print data
    return HttpResponse('Okay')