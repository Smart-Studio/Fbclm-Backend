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

from rest_framework import serializers

from fixtures.models import Season, League, Group, SubGroup, Team, MatchDay, Fixture, KnockoutGroup, Knockout, TableRow


class TableRowSerializer(serializers.ModelSerializer):
    played = serializers.Field()
    diff = serializers.Field()

    class Meta:
        model = TableRow
        fields = ('id', 'team', 'played', 'won', 'lost', 'scored', 'against', 'diff')


class FixtureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fixture
        fields = ('id', 'home_team', 'home_score', 'away_team', 'away_score', 'date')


class MatchDaySerializer(serializers.ModelSerializer):
    fixtures = FixtureSerializer(many=True)

    class Meta:
        model = MatchDay
        fields = ('id', 'date', 'fixtures')


class KnockoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Knockout
        fields = ('id', 'stage')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name')


class SubGroupSerializer(serializers.ModelSerializer):
    match_days = MatchDaySerializer(many=True)

    class Meta:
        model = SubGroup
        fields = ('id', 'name', 'match_days')


class KnockoutGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnockoutGroup
        field = ('name', 'venue', )


class GroupSerializer(serializers.ModelSerializer):
    # subgroups = SubGroupsSerializer(many=True)
    # match_days = MatchDaySerializer(many=True)

    class Meta:
        model = Group
        fields = ('id', 'name')
        # 'subgroups', 'match_days'


class GroupDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', )


class LeagueSerializer(serializers.ModelSerializer):
    # groups = GroupSerializer(many=True)
    # teams = TeamSerializer(many=True)

    class Meta:
        model = League
        fields = ('id', 'name')


class LeagueDetailSerializer(serializers.ModelSerializer):
    # groups = GroupSerializer(many=True)
    # teams = TeamSerializer(many=True)

    class Meta:
        model = League
        fields = ('name',)


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ('id', 'season_name')

