// Generated by CoffeeScript 1.6.3
(function() {
  require(['../main'], function(main) {
    return require(['domReady', 'jquery', 'typeahead', 'ractive', 'underscore', 'text!app/index.template'], function(ready, $, typeahead, Ractive, _, template) {
      var r;
      r = new Ractive({
        el: 'app',
        template: template
      });
      return $.getJSON('/api/v1/set/', {
        format: 'json',
        order_by: '-id'
      }, function(data) {
        console.log(r.get('sets'));
        r.set('sets', data.objects);
        return console.log(r.get('sets'));
      });
    });
  });

}).call(this);
