define [
	'jquery',
	'typeahead'
	'underscore'
	],
	($, typeahead, _) ->
		console.log 'Preparing autcomplete'
		
		(input_id, game_title_id) ->
			options = data:
						format: 'json'
			if (game_title_id)
				options = _(options).extend({
					games__id: game_title_id
				})
			
			$.ajaxSetup(options)
			
			$(input_id).typeahead(
				prefetch:
					url: '/api/v1/character'
					filter: (data) ->
						data.objects
				valueKey: 'name'
			)