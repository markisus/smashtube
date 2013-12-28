require ['../main'], 
(main) ->
	require [
		'domReady',
		'jquery',
		'typeahead',
		'ractive',
		'underscore',
		'text!app/index.template'], 
	(ready, $, typeahead, Ractive, _, template) ->
		
		r = new Ractive(
			el: 'app'
			template: template
		)
		
		$.getJSON '/api/v1/tournament/',
			format: 'json',
			(data) ->
				tournaments = data.objects
				r.set('tournaments', tournaments)
		
		$.getJSON '/api/v1/player/',
			format: 'json',
			(data) ->
				players = data.objects
				r.set('players', players)
	
		r.on 'add-tournament', (event) ->
			r.set 'adding_tournament', true
		r.on 'cancel-add-tournament', (event) ->
			r.set 'adding_tournament', false
		r.on 'submit-tournament', (event) ->
			data =
				name: r.get('tournament_name')
				date: r.get('tournament_date')
				location: r.get('tournament_location')
			data = JSON.stringify data
			req = $.ajax
				type: 'POST',
				url: '/api/v1/tournament/', 
				data: data,
				dataType: 'text',
				contentType: 'application/json'
			req.done (data) ->
				console.log 'done', data
				location = req.getResponseHeader 'Location'
				console.log 'Location', location
				r.set 'adding_tournament', false
				r.set 'tournament_name', undefined
				r.set 'tournament_date', undefined
				r.set 'tournament_location', undefined
				$.getJSON location,
					format: 'json'
					(data) ->
						console.log 'newly created:', data
						tournaments = r.get 'tournaments'
						tournaments.push data
						
			req.fail (data) ->
				errors = JSON.parse req.responseText
				r.set 'tournament_errors', errors
				
		r.on 'edit-tournament', (event) ->
			r.set event.keypath + '.old_name', event.context.name
			r.set event.keypath + '.old_date', event.context.date
			r.set event.keypath + '.old_location', event.context.location
			r.set event.keypath + '.editing', true
			
		r.on 'cancel-edit-tournament', (event) ->
			r.set event.keypath + '.name', event.context.old_name
			r.set event.keypath + '.date', event.context.old_date
			r.set event.keypath + '.location', event.context.old_location
			r.set event.keypath + '.editing', false
			
		r.on 'save-tournament', (event) ->
			console.log event
			console.log 'saving'
			data =
				name: event.context.name
				date: event.context.date
				location: event.context.location
			data = JSON.stringify data
			console.log data
			req = $.ajax
				type: 'PUT',
				url: event.context.resource_uri,
				data: data,
				dataType: 'text',
				contentType: 'application/json'
			req.done () ->
				r.set event.keypath + '.editing', false
				
		r.on 'delete-tournament', (event) ->
			console.log 'delete', event
			delete_okay = confirm('Are you sure you want to delete ' + event.context.name + '?')
			if delete_okay
				req = $.ajax
					type: 'DELETE'
					url: event.context.resource_uri
				req.done () ->
					console.log 'splicing'
					tournaments = r.get('tournaments')
					console.log tournaments
					tournaments.splice(event.index.tournament_index, 1)
					
		#----------------
		r.on 'add-player', (event) ->
			r.set 'adding_player', true
		r.on 'cancel-add-player', (event) ->
			r.set 'adding_player', false
		r.on 'submit-player', (event) ->
			data =
				handle: r.get('player_handle')
				first_name: r.get('player_first_name')
				last_name: r.get('player_last_name')
			data = JSON.stringify data
			req = $.ajax
				type: 'POST',
				url: '/api/v1/player/', 
				data: data,
				dataType: 'text',
				contentType: 'application/json'
			req.done (data) ->
				console.log 'done', data
				location = req.getResponseHeader 'Location'
				console.log 'Location', location
				r.set 'adding_player', false
				r.set 'player_handle', undefined
				r.set 'player_first_name', undefined
				r.set 'player_last_name', undefined
				$.getJSON location,
					format: 'json'
					(data) ->
						console.log 'newly created:', data
						players = r.get 'players'
						players.push data
						
			req.fail (data) ->
				errors = JSON.parse req.responseText
				r.set 'player_errors', errors
				
		r.on 'edit-player', (event) ->
			r.set event.keypath + '.old_handle', event.context.handle
			r.set event.keypath + '.old_first_name', event.context.first_name
			r.set event.keypath + '.old_last_name', event.context.last_name
			r.set event.keypath + '.editing', true
			
		r.on 'cancel-edit-player', (event) ->
			r.set event.keypath + '.handle', event.context.old_handle
			r.set event.keypath + '.first_name', event.context.old_first_name
			r.set event.keypath + '.last_name', event.context.old_last_name
			r.set event.keypath + '.editing', false
			
		r.on 'save-player', (event) ->
			console.log event
			console.log 'saving'
			data =
				handle: event.context.handle
				first_name: event.context.first_name
				last_name: event.context.last_name
			data = JSON.stringify data
			console.log data
			req = $.ajax
				type: 'PUT',
				url: event.context.resource_uri,
				data: data,
				dataType: 'text',
				contentType: 'application/json'
			req.done () ->
				r.set event.keypath + '.editing', false
				
		r.on 'delete-player', (event) ->
			console.log 'delete', event
			delete_okay = confirm('Are you sure you want to delete ' + event.context.handle + '?')
			if delete_okay
				req = $.ajax
					type: 'DELETE'
					url: event.context.resource_uri
				req.done () ->
					console.log 'splicing'
					players = r.get('players')
					players.splice(event.index.player_index, 1)