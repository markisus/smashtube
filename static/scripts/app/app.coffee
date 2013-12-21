require ['../main'], 
(main) ->
	require [
		'domReady',
		'jquery',
		'ractive',
		'underscore',
		'text!app/app.template'], 
	(ready, $, Ractive, _, template) ->
		
		r = new Ractive(
			el: 'app'
			template: template
		)
		
		r.set('step', 'link-entry')
		
		r.observe 'link', (link, previous) ->
			if not link
				r.set('error', 'Link field is blank!')
			else
				r.set('error', undefined)
					
		r.on 'select-link', (event) ->
			link = r.get('link')
			
			$.getJSON '/api/v1/video-url/', 
				format: 'json',
				video_url: link,
				(data) ->
					console.log data
					post_data = JSON.stringify {video_url: link}
					if not data.objects.length
						$.ajax
							type: 'POST',
							url: '/api/v1/video-url/', 
							data: post_data,
							dataType: 'application/json',
							contentType: 'application/json'
			
			r.set('step', 'tournament-entry')
		
		# Tournament Select
		r.observe 'step', (new_step, old_step) ->
			if new_step == 'tournament-entry'
				$.getJSON '/api/v1/tournament/',
				format: 'json',
				(data) ->
					tournaments = data.objects
					console.log tournaments
					r.set('tournaments', tournaments)
					
		r.on 'new-tournament', (event) ->
			tournament = r.get('tournament')

			post_data = JSON.stringify {name: tournament}

			req = $.ajax
				type: 'POST',
				url: '/api/v1/tournament/', 
				data: post_data,
				dataType: 'application/json',
				contentType: 'application/json'
			
			req.done () ->
				r.set('step', 'set-entry')
			req.fail () ->
				r.set('error', req.responseText)
		
		r.observe 'tournament', (current, last) ->
			r.set('error', undefined)
			tournament = r.get('tournament')
			tournaments = r.get('tournaments')
			tournament_found = _(tournaments).find (t) ->
				t.name == tournament
			if tournament_found
				r.set('error', 'This tournament already exists (see the list below)')
			