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
		
		$.getJSON '/api/v1/set/',
				format: 'json',
				order_by: '-id',
				(data) ->
					sets = data.objects
					for set in sets						
						teams = _(set.player_sessions).groupBy((ps) -> ps.team).value()
						set.teams = teams
					console.log sets
					r.set('sets', data.objects)