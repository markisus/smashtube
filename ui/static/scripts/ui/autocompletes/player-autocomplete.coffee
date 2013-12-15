define [
	'jquery',
	'typeahead'
	],
	($, typeahead) ->
		console.log 'Preparing autcomplete'
		(input_id) ->
			$.ajaxSetup(
				data:
					format: 'json'
			)
			console.log "Binding autocomplete to", input_id
			console.log "Finding dom element", $(input_id)
			$(input_id).typeahead(
				prefetch:
					url: '/api/v1/player'
					filter: (data) ->
						data.objects
				valueKey: 'name'
			)