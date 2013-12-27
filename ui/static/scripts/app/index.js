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
        var set, sets, teams, _i, _len;
        sets = data.objects;
        for (_i = 0, _len = sets.length; _i < _len; _i++) {
          set = sets[_i];
          teams = _(set.player_sessions).groupBy(function(ps) {
            return ps.team;
          }).value();
          set.teams = teams;
        }
        console.log(sets);
        return r.set('sets', data.objects);
      });
    });
  });

}).call(this);
