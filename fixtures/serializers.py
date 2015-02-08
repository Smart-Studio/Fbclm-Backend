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

