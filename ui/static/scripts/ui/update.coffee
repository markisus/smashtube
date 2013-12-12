require ['../main'], 
(main) ->
	require(['ui/chooser/chooser', 'domReady', 'jquery'], (chooser, domReady, $) ->
		domReady () ->
			console.log "Hello there. This is the main!"

			createTournament = (latent_tournament) ->
				f = $.ajax
					url: '/api/v1/tournament/'
					type: 'POST'
					contentType: 'application/json'
					data: JSON.stringify(latent_tournament)
				f.done (data) ->
					console.log 'Done'
					console.log data
				f.fail (jqXHR) ->
					if jqXHR.responseJSON.error_message?
						console.log "Error", jqXHR.responseJSON.error_message
					else
						console.log "Unknown error"
			
			chooser
				el:'tournament-chooser', 
				query_url:'/api/v1/tournament/?name__icontains=',
				onSelect: (e) -> console.log 'Select', e
				form_style: 'pure-form pure-form-stacked'
				item_style: 'pure-button pure-button-primary',
				placeholder: 'tournament name'
				legend: 'Create or Choose Tournament'
				allow_new: true
				onNew: (e) -> createTournament e
				allow_input: false
	)