require ['../main'], 
(main) ->
	require [
		'domReady',
		'jquery',
		'typeahead',
		'ractive',
		'underscore',
		'fuzzyset',
		'text!app/app.template'], 
	(ready, $, typeahead, Ractive, _, FuzzySet, template) ->
		
		r = new Ractive(
			el: 'app'
			template: template
			decorators: 
				tournament_typeahead: (node) ->
					ractive = node._ractive.root;
					keypath = node._ractive.binding.keypath;
					
					$(node).typeahead(
						prefetch:
							url: '/api/v1/tournament/?format=json&limit=0'
							filter: (data) ->
								data.objects
						valueKey: 'name'
					).on( 'typeahead:selected typeahead:autocompleted', ( event, datum ) ->
						ractive.set('tournament', datum.name)
					)
				
					teardown:  () ->
						$(node).typehead('destroy')
			
			data:
				length_gt_1: (t) ->
					t.length > 1
		)
		
		r.on 'next', (event) ->
			step = r.get('step')
			if step == 'link-entry'
				r.set('step', 'tournament-entry')
			if step == 'tournament-entry'
				r.set('step', 'set-entry')
			if step == 'set-entry'
				r.set('step', 'match-entry')
			if step == 'match-entry'
				console.log 'going to final'
				r.set('step', 'final')
		r.on 'back', (event) ->
			step = r.get('step')
			if step == 'final'
				r.set('step', 'match-entry')
			if step == 'match-entry'
				console.log 'match entry detected'
				r.set('step', 'set-entry')
			if step == 'set-entry'
				r.set('step', 'tournament-entry')
			if step == 'tournament-entry'
				r.set('step', 'link-entry')
		
		r.set('step', 'link-entry')
		
		r.observe 'step', (new_step, old_step) ->
			r.set 'error', undefined
			
			if new_step == 'tournament-entry'
			#Populate tournament data
				$.getJSON '/api/v1/tournament/',
				format: 'json',
				(data) ->
					tournaments = data.objects
					r.set('tournaments', tournaments)
					r.set('tournament', '')
					
			if new_step == 'set-entry'
			#Populate game titles
				$.getJSON 'api/v1/game-title',
				format: 'json',
				(data) ->
					game_titles = data.objects
					r.set('game_titles', game_titles)
				r.set('game_title', 'Melee')
			
			if new_step == 'match-entry'
				r.set('num_matches', 1)
				r.set('teams',
					[[{character:'', player:''}], [{character:'', player:''}]])
				game_title = r.get('game_title')

				$.getJSON 'api/v1/character/',
				games__name: game_title
				limit: '0'
				format: 'json',
				(data) ->
					characters = _(data.objects).sortBy((c) -> c.name).value()
					r.set('characters', characters)
					r.set('default_character', characters[0])
					
			if new_step == 'final'
				# Package the data
				link = r.get('link') or ''
				tournament = r.get('tournament') or ''
				game_title = r.get('game_title')
				set_description = r.get('set_description') or ''
				num_matches = parseInt(r.get('num_matches'))
				teams = r.get('teams')
				
				post_data = JSON.stringify(
					link: link
					tournament: tournament
					game_title: game_title
					set_description: set_description
					num_matches: num_matches
					teams: teams)
					
				$.ajax
					type: 'POST',
					url: '/submit-link/', 
					data: post_data,
					dataType: 'application/json',
					contentType: 'application/json'
					
		r.observe 'link', (link, previous) ->
			if not link
				r.set('error', 'Link field is blank!')
			else
				r.set('error', undefined)
					
		r.on 'select-link', (event) ->
			r.set('step', 'tournament-entry')
		
		# Tournament Select
			
		r.on 'new-tournament', (event) ->
			tournament = r.get('tournament')

			post_data = JSON.stringify {name: tournament}
			req = $.ajax
				type: 'POST',
				url: '/api/v1/tournament/', 
				data: post_data,
				dataType: 'text',
				contentType: 'application/json'
			
			req.done () ->
				r.set('step', 'set-entry')
				
			req.fail () ->
				r.set('error', req.responseText)
		
		r.on 'select-tournament', (event) ->
			r.set('tournament', event.context)
		
		# Set Select
			
		r.on 'set-description-suggestion', (event, description) ->
			r.set('set_description', description)
			r.set('suggestion', undefined)
			
		# Match Entry
		
		r.on 'another-player', (event) ->
			team = r.get(event.keypath)
			default_character = r.get('default_character')
			team.push {player:'', character:default_character.name}
			
		r.on 'fewer-players', (event) ->
			team = r.get(event.keypath)
			team.pop()

		r.on 'select-character', (event) ->
			team_number = event.index.team_number
			player_number = event.index.player_number
			keypath = 'teams.' + team_number + '.' + player_number
			r.set(keypath + '.character', event.context.name)
			r.set(keypath + '.suggestion', undefined)
			
		r.observe 'teams', (current, old) ->
			teams = current
			for team in teams
				for player in team
					if player.player?.length < 1
						console.log 'Found an empty player'
						r.set('error', 'One or more player names are empty')
						return
			r.set('error', undefined)