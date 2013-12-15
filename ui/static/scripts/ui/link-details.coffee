require ['../main'], 
(main) ->
	require [
		'domReady',
		'ractive',
		'text!ui/set-list.template',
		'ui/autocompletes/game-title-autocomplete'], (ready, R, template, gtauto) ->
        
		$.ajaxSetup data:
						csrfmiddlewaretoken: csrf_token
		
		gtauto('#tournament')
		
		###
		$('#tournament').typeahead(
			prefetch: 
				url: '/api/v1/tournament'
				filter: (data) ->
					console.log data.objects
					data.objects
			valueKey: 'name'
		)
		###
		
		sets_related_to_video = (video_url_id, success) ->
			console.log 'About to do the query'
			query = '/api/v1/set/'
			$.getJSON query, {
				matches__video_url__id: video_url_id,
				format: 'json'
			}, success
		
		console.log 'Hello world!'
		console.log video_url_id
		console.log 'Finding sets...'

		sets_related_to_video video_url_id, (data) ->
			console.log 'Got some data', data.objects
			sets = data.objects
			
			window.r = new R(
				el: 'set-list'
				template: template
				data:
					sets: sets
					is_last_match: (set_index, match_index) ->
						set_index = parseInt(set_index)
						match_index = parseInt(match_index)
						sets[set_index]?.matches[match_index+1] == undefined
			)
			
			refresh_match = (event) ->
				set_index = parseInt(event.index.set_index)
				match_index = parseInt(event.index.match_index)
				console.log "sets are", sets, set_index, match_index
				match = sets[set_index].matches[match_index]
				
				query = '/api/v1/match/' + match.id
				request = $.getJSON query,
					format: 'json'
				request.done (data) ->
					r.set('sets.' + set_index + '.matches.' + match_index, data)
					console.log "Refreshed", data
			
			refresh_set = (event) ->
				set_index = parseInt(event.index.set_index)
				set = sets[set_index]
				
				query = '/api/v1/set/' + set.id
				request = $.getJSON query,
					format: 'json'
				request.done (data) ->
					r.set('sets.' + set_index, data)
			
			r.on 'add-player', (event) ->
				context = event.context
				request = $.post '/submit-player-for-match', 
					character_name: context.character
					player_name: context.player
					match_id: context.id
				request.done (data) ->
					refresh_match(event)
				request.fail (data) ->
					r.set(event.keypath + '.error', '! ' + data.responseText)
			
			r.on 'delete-player', (event) ->
				console.log 'deleting', event
				context = event.context
				request = $.post '/delete-player-session',
					player_session_id: event.context.id
				request.done (data) ->
					refresh_match(event)
					
			r.on 'hide-set', (event) ->
				console.log 'hiding'
				current = r.get(event.keypath + '.hidden')
				console.log 'current', current
				console.log 'keypath', event.keypath
				r.set(event.keypath + '.hidden', !current)
				
			r.on 'edit-match', (event, editing) ->
				if not editing
					r.set(event.keypath + '.editing', true)
				else
					context = event.context
					request = $.post '/edit-match',
						match_id: context.id
						start: context.start
						end: context.end
						index: context.index
					request.done (data) ->
						r.set(event.keypath + '.editing', false)
					request.fail (data) ->
						r.set(event.keypath + '.error', data.responseText)
			
			r.on 'copy-match', (event) ->
				context = event.context
				set_index = parseInt(event.index['set_index'])
				set = sets[set_index]
				num_matches = set.matches.length
				console.log set_index, set, num_matches
				request = $.post '/copy-match',
					match_id: set.matches[num_matches-1].id
				request.done (data) ->
					refresh_set(event)
		
			r.on 'delete-match', (event) ->
				context = event.context
				request = $.post '/delete-match',
					match_id: context.id
				request.done (data) ->
					refresh_set(event)
				