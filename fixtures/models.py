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


class KnockoutGroup(Group):
    venue = models.CharField(max_length=100)


class SubGroup(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group)


class Team(models.Model):
    league = models.ForeignKey(League)
    name = models.CharField(max_length=100)
    badge = models.URLField(null=True)


class MatchDay(models.Model):
    date = models.DateTimeField()
    group = models.ForeignKey(Group, null=True, blank=True)
    subgroup = models.ForeignKey(SubGroup, null=True, blank=True)


class Knockout(models.Model):
    stage = models.CharField(max_length=100)
    group = models.ForeignKey(KnockoutGroup)


class Fixture(models.Model):
    match_day = models.ForeignKey(MatchDay, null=True, blank=True)
    knockout = models.ForeignKey(Knockout, null=True, blank=True)
    home_team = models.ForeignKey(Team, related_name="home_team")
    home_score = models.IntegerField(default=0)
    away_team = models.ForeignKey(Team, related_name="away_team")
    away_score = models.IntegerField(default=0)
    date = models.DateTimeField(null=True, blank=True)


class TableRow(models.Model):
    match_day = models.ForeignKey(MatchDay)
    team = models.ForeignKey(Team)
    won = models.IntegerField()
    lost = models.IntegerField()
    scored = models.IntegerField()
    against = models.IntegerField()

    @property
    def played(self):
        return self.won + self.lost

    @property
    def diff(self):
        return self.scored - self.against
