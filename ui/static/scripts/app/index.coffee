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
					console.log r.get('sets')
					r.set('sets', data.objects)
					console.log r.get('sets')