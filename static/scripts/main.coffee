requirejs.config
	baseUrl: '/static/scripts'
	paths:
		jquery: 'jquery-2.0.3.min'
		underscore: 'lodash.min'
		ractive: 'Ractive'
		throttle: 'jquery-throttle.min'
		typeahead: 'typeahead.min'
		fuzzyset: 'fuzzyset'
	shim:
		typeahead:
			deps: ['jquery']
		throttle:
			deps: ['jquery']
console.log 'Loaded main config'