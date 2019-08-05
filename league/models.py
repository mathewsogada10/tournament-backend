from django.db import models
from datetime import datetime

# Create your models here.
class League(models.Model):
    name = models.CharField(max_length = 50)
    createdAt = models.DateTimeField(default = datetime.now(),blank = True)

    def __str__(self):
        return self.name

    @property
    def owner(self):
        return self.user

class LeagueStage(models.Model):
    name = models.CharField(max_length = 30)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    seasonStart = models.DateField(default = datetime.now(),blank = True)
    seasonEnd = models.DateField(default = datetime.now(),blank = True)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length = 50)
    def __str__(self):
        return self.name

class TeamStage(models.Model):
    team = models.ForeignKey(Team, on_delete = models.CASCADE)
    stage = models.ForeignKey(LeagueStage,related_name='teamStages', on_delete = models.CASCADE)
    points = models.IntegerField(default = 0)
    goalScored = models.IntegerField(default = 0)
    goalConceded = models.IntegerField(default = 0)
    goalDiff = models.IntegerField(default = 0)
    gamesPlayed = models.IntegerField(default = 0)

    def __str__(self):
        return self.team.name + " ["+ self.stage.name +"]"

class fixtures(models.Model):
    homeTeam = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='homeTeams')
    awayTeam = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='awayTeams')
    createdAt = models.DateTimeField(default = datetime.now(),blank = True)
    matchDate = models.DateTimeField(default = datetime.now(),blank = True)
    homeTeamGoal = models.IntegerField(default = 0)
    awayTeamGoal = models.IntegerField(default = 0)
    stage = models.ForeignKey(LeagueStage, on_delete = models.CASCADE,related_name='stage')

    def __str__(self):
        return "{} - {} [ {} : {} ]".format(self.homeTeam.name,self.awayTeam.name,self.homeTeamGoal,self.awayTeamGoal)
