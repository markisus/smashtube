require ['/static/scripts/main.js'],
(main) ->
	require ['ractive', 'domReady', 'text!ui/scratch/scratch.template'], (R, ready, template) ->
		data = {
			"items": [
				{"name": "red"},
				{"name": "green"},
				{"name": "blue"}
				]
		}
		
		r = new R(
			el: 'scratch'
			template: template
			data: data
		)
		
		r.on 'loaded', (event) ->
			console.log 'Loaded!'

