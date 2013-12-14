require ['../main'], 
(main) ->
	require [
		'jquery', 
		'ractive',
		'text!ui/set-list.template'], ($, R, template) ->
		sets_related_to_video = (video_url_id, success) ->
			console.log 'About to do the query'
			query = '/api/v1/set/'
			$.getJSON query, {
				match__video_url: video_url_id,
				format: 'json'
			}, success
		
		console.log 'Hello world!'
		console.log video_url_id
		console.log 'Finding sets...'

		sets_related_to_video video_url_id, (data) ->
			console.log 'Got some data', data.objects

			window.r = new R(
				el: 'set-list'
				template: template
				data:
					sets: data.objects
					greeting: 'hello!'
			)