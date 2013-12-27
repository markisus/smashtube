// Generated by CoffeeScript 1.6.3
(function() {
  require(['../main'], function(main) {
    return require(['domReady', 'jquery', 'typeahead', 'ractive', 'underscore', 'fuzzyset', 'text!app/app.template'], function(ready, $, typeahead, Ractive, _, FuzzySet, template) {
      var r;
      r = new Ractive({
        el: 'app',
        template: template,
        decorators: {
          tournament_typeahead: function(node) {
            var keypath, ractive;
            ractive = node._ractive.root;
            keypath = node._ractive.binding.keypath;
            $(node).typeahead({
              prefetch: {
                url: '/api/v1/tournament/?format=json&limit=0',
                filter: function(data) {
                  return data.objects;
                }
              },
              valueKey: 'name'
            }).on('typeahead:selected typeahead:autocompleted', function(event, datum) {
              return ractive.set('tournament', datum.name);
            });
            return {
              teardown: function() {
                return $(node).typehead('destroy');
              }
            };
          }
        },
        data: {
          length_gt_1: function(t) {
            return t.length > 1;
          }
        }
      });
      r.on('next', function(event) {
        var step;
        step = r.get('step');
        if (step === 'link-entry') {
          r.set('step', 'tournament-entry');
        }
        if (step === 'tournament-entry') {
          r.set('step', 'set-entry');
        }
        if (step === 'set-entry') {
          r.set('step', 'match-entry');
        }
        if (step === 'match-entry') {
          console.log('going to final');
          return r.set('step', 'final');
        }
      });
      r.on('back', function(event) {
        var step;
        step = r.get('step');
        if (step === 'final') {
          r.set('step', 'match-entry');
        }
        if (step === 'match-entry') {
          console.log('match entry detected');
          r.set('step', 'set-entry');
        }
        if (step === 'set-entry') {
          r.set('step', 'tournament-entry');
        }
        if (step === 'tournament-entry') {
          return r.set('step', 'link-entry');
        }
      });
      r.set('step', 'link-entry');
      r.observe('step', function(new_step, old_step) {
        var game_title, link, num_matches, post_data, set_description, teams, tournament;
        r.set('error', void 0);
        if (new_step === 'tournament-entry') {
          $.getJSON('/api/v1/tournament/', {
            format: 'json'
          }, function(data) {
            var tournaments;
            tournaments = data.objects;
            r.set('tournaments', tournaments);
            return r.set('tournament', '');
          });
        }
        if (new_step === 'set-entry') {
          $.getJSON('api/v1/game-title', {
            format: 'json'
          }, function(data) {
            var game_titles;
            game_titles = data.objects;
            return r.set('game_titles', game_titles);
          });
          r.set('game_title', 'Melee');
        }
        if (new_step === 'match-entry') {
          r.set('num_matches', 1);
          r.set('teams', [
            [
              {
                character: '',
                player: ''
              }
            ], [
              {
                character: '',
                player: ''
              }
            ]
          ]);
          game_title = r.get('game_title');
          $.getJSON('api/v1/character/', {
            games__name: game_title,
            limit: '0',
            format: 'json'
          }, function(data) {
            var characters;
            characters = _(data.objects).sortBy(function(c) {
              return c.name;
            }).value();
            r.set('characters', characters);
            return r.set('default_character', characters[0]);
          });
        }
        if (new_step === 'final') {
          link = r.get('link') || '';
          tournament = r.get('tournament') || '';
          game_title = r.get('game_title');
          set_description = r.get('set_description') || '';
          num_matches = parseInt(r.get('num_matches'));
          teams = r.get('teams');
          post_data = JSON.stringify({
            link: link,
            tournament: tournament,
            game_title: game_title,
            set_description: set_description,
            num_matches: num_matches,
            teams: teams
          });
          return $.ajax({
            type: 'POST',
            url: '/submit-link/',
            data: post_data,
            dataType: 'application/json',
            contentType: 'application/json'
          });
        }
      });
      r.observe('link', function(link, previous) {
        if (!link) {
          return r.set('error', 'Link field is blank!');
        } else {
          return r.set('error', void 0);
        }
      });
      r.on('select-link', function(event) {
        return r.set('step', 'tournament-entry');
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
          dataType: 'text',
          contentType: 'application/json'
        });
        req.done(function() {
          return r.set('step', 'set-entry');
        });
        return req.fail(function() {
          return r.set('error', req.responseText);
        });
      });
      r.on('select-tournament', function(event) {
        return r.set('tournament', event.context);
      });
      r.on('set-description-suggestion', function(event, description) {
        r.set('set_description', description);
        return r.set('suggestion', void 0);
      });
      r.on('another-player', function(event) {
        var default_character, team;
        team = r.get(event.keypath);
        default_character = r.get('default_character');
        return team.push({
          player: '',
          character: default_character.name
        });
      });
      r.on('fewer-players', function(event) {
        var team;
        team = r.get(event.keypath);
        return team.pop();
      });
      r.on('select-character', function(event) {
        var keypath, player_number, team_number;
        team_number = event.index.team_number;
        player_number = event.index.player_number;
        keypath = 'teams.' + team_number + '.' + player_number;
        r.set(keypath + '.character', event.context.name);
        return r.set(keypath + '.suggestion', void 0);
      });
      return r.observe('teams', function(current, old) {
        var player, team, teams, _i, _j, _len, _len1, _ref;
        teams = current;
        for (_i = 0, _len = teams.length; _i < _len; _i++) {
          team = teams[_i];
          for (_j = 0, _len1 = team.length; _j < _len1; _j++) {
            player = team[_j];
            if (((_ref = player.player) != null ? _ref.length : void 0) < 1) {
              console.log('Found an empty player');
              r.set('error', 'One or more player names are empty');
              return;
            }
          }
        }
        return r.set('error', void 0);
      });
    });
  });

}).call(this);
