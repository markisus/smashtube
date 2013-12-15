define [
	'jquery',
	'typeahead'
	],
	($, typeahead) ->
		console.log 'Preparing autcomplete'
		(input_id, game_title_id) ->
			$.ajaxSetup(
				data:
					format: 'json'
			)
			console.log "Binding autocomplete to", input_id
			console.log "Finding dom element", $(input_id)
			$(input_id).typeahead(
				prefetch:
					url: '/api/v1/character'
					filter: (data) ->
						data.objects
				valueKey: 'name'
			)