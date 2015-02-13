"""
Copyright 2015 Smart Studio.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from django.db import models


class Season(models.Model):
    season_name = models.CharField(max_length=100)

    def __str__(self):
        return self.season_name


class League(models.Model):
    name = models.CharField(max_length=100)
    season = models.ForeignKey(Season, related_name='leagues')

    def __str__(self):
        return self.name + self.season


class Group(models.Model):
    name = models.CharField(max_length=100)
    league = models.ForeignKey(League, related_name='groups')

    def __str__(self):
        return self.name + self.league


class KnockoutGroup(Group):
    venue = models.CharField(max_length=100)


class SubGroup(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, related_name='subgroups')


class Team(models.Model):
    league = models.ForeignKey(League, related_name='teams')
    name = models.CharField(max_length=100)
    badge = models.URLField(null=True)


class MatchDay(models.Model):
    date = models.DateTimeField()
    group = models.ForeignKey(Group, null=True, blank=True, related_name='match_days')
    subgroup = models.ForeignKey(SubGroup, null=True, blank=True, related_name='match_days')


class Knockout(models.Model):
    stage = models.CharField(max_length=100)
    group = models.ForeignKey(KnockoutGroup)


class Fixture(models.Model):
    match_day = models.ForeignKey(MatchDay, null=True, blank=True, related_name='fixtures')
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
