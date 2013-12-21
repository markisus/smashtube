// Generated by CoffeeScript 1.6.3
(function() {
  require(['../main'], function(main) {
    return require(['domReady', 'jquery', 'ractive', 'underscore', 'text!app/app.template'], function(ready, $, Ractive, _, template) {
      var r;
      r = new Ractive({
        el: 'app',
        template: template
      });
      r.set('step', 'link-entry');
      r.observe('link', function(link, previous) {
        if (!link) {
          return r.set('error', 'Link field is blank!');
        } else {
          return r.set('error', void 0);
        }
      });
      r.on('select-link', function(event) {
        var link;
        link = r.get('link');
        $.getJSON('/api/v1/video-url/', {
          format: 'json',
          video_url: link
        }, function(data) {
          var post_data;
          console.log(data);
          post_data = JSON.stringify({
            video_url: link
          });
          if (!data.objects.length) {
            return $.ajax({
              type: 'POST',
              url: '/api/v1/video-url/',
              data: post_data,
              dataType: 'application/json',
              contentType: 'application/json'
            });
          }
        });
        return r.set('step', 'tournament-entry');
      });
      r.observe('step', function(new_step, old_step) {
        if (new_step === 'tournament-entry') {
          return $.getJSON('/api/v1/tournament/', {
            format: 'json'
          }, function(data) {
            var tournaments;
            tournaments = data.objects;
            console.log(tournaments);
            return r.set('tournaments', tournaments);
          });
        }
      });
      r.on('new-tournament', function(event) {
        var post_data, req, tournament;
        tournament = r.get('tournament');
        post_data = JSON.stringify({
          name: tournament
        });
        req = $.ajax({
          type: 'POST',
          url: '/api/v1/tournament/',
          data: post_data,
          dataType: 'application/json',
          contentType: 'application/json'
        });
        req.done(function() {
          return r.set('step', 'set-entry');
        });
        return req.fail(function() {
          return r.set('error', req.responseText);
        });
      });
      return r.observe('tournament', function(current, last) {
        var tournament, tournament_found, tournaments;
        r.set('error', void 0);
        tournament = r.get('tournament');
        tournaments = r.get('tournaments');
        tournament_found = _(tournaments).find(function(t) {
          return t.name === tournament;
        });
        if (tournament_found) {
          return r.set('error', 'This tournament already exists (see the list below)');
        }
      });
    });
  });

}).call(this);
