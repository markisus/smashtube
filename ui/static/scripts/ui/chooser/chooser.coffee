define [
	'ractive', 
	'jquery', 
	'underscore', 
	'text!ui/chooser/chooser.template'
	], 
	(Ractive, $, _, template) ->
		return (options) ->
			el = options.el
			query_url = options.query_url
			onSelect = options.onSelect
			styles = options.styles
			placeholder = options.placeholder
			form_style = options.form_style
			item_style = options.item_style
			allow_new = options.allow_new
			onNew = options.onNew
			legend = options.legend

			console.log "This is the chooser!"
			suggester = (query, callback) ->
				$.ajax
					url: query_url + query
					type: 'GET'
					accepts:
						json: 'application/json'
				.done (result) ->
					callback(result.objects)
			
			console.log "allow input", options.allow_input
			console.log "template", template
			r = new Ractive(
				el: el
				template: template
				data:
					suggestions: []
					filter_value: ''
					legend: legend
					placeholder: placeholder
					form_style: options.form_style
					item_style: options.item_style
			)
			r.observe 'filter_value', (t) ->
				suggester(t, (results) ->
					results = _(results).sortBy((r) -> r.name).value()
					current = 
						name: r.get('filter_value')
					if current.name and !_(results).find((t)->t.name.toLowerCase()==current.name.toLowerCase()) and allow_new
						results.unshift current;
					r.set 'suggestions', results;
				)
			r.on 'select', (event) ->
				thing = event.context
				if thing.id?
					onSelect(thing)
				else
					onNew(thing)
			r