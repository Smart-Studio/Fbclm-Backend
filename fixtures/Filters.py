import rest_framework_filters as filters
from fixtures.models import League, Group, SubGroup

__author__ = 'juanyanezgc'


class LeaguesFilter(filters.FilterSet):
    season = filters.NumberFilter(name='season_id')

    class Meta:
        model = League
        fields = ['season']


class GroupsFilter(filters.FilterSet):
    league = filters.NumberFilter(name='league_id')

    class Meta:
        model = Group
        fields = ['league']


class SubGroupsFilter(filters.FilterSet):
    league = filters.NumberFilter(name='league_id')

    class Meta:
        model = SubGroup
        fields = ['league']
