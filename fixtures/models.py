from django.db import models


class Season(models.Model):
    season_name = models.CharField(max_length=100)

    def __str__(self):
        return self.season_name


class League(models.Model):
    name = models.CharField(max_length=100)
    season = models.ForeignKey(Season)


class Group(models.Model):
    name = models.CharField(max_length=100)
    league = models.ForeignKey(League)


class SubGroup(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group)


class Team(models.Model):
    league = models.ForeignKey(League)
    name = models.CharField(max_length=100)
    badge = models.URLField()


class MatchDay(models.Model):
    date = models.DateTimeField()
    league = models.ForeignKey(League)


class Fixture(models.Model):
    match_day = models.ForeignKey(MatchDay)
    home_team = models.ForeignKey(Team, related_name="home_team")
    home_score = models.IntegerField(default=0)
    away_team = models.ForeignKey(Team, related_name="away_team")
    away_score = models.IntegerField(default=0)
    date = models.DateTimeField()
