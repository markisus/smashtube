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