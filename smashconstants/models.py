from django.db import models

class GameTitle(models.Model):
    name = models.CharField(
                            unique=True,
                            null=False, 
                            blank=False, 
                            max_length=70)
    
    def __unicode__(self):
        return self.name

class Character(models.Model):
    name = models.CharField(null=False, blank=False, max_length=20)
    games = models.ManyToManyField(GameTitle)

    def __unicode__(self):
        return self.name

class CharacterIcon(models.Model):
    icon = models.URLField(blank=False, null=False)
    character = models.ForeignKey(Character)
    game = models.ForeignKey(GameTitle)

    def __unicode__(self):
        return self.icon