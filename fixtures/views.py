from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin, DetailSerializerMixin

from fixtures.filters import LeaguesFilter, GroupsFilter, SubGroupsFilter
from fixtures.models import Season, League, Group, SubGroup, Team, KnockoutGroup, Knockout, MatchDay, Fixture, TableRow
from fixtures.serializers import SeasonSerializer, LeagueSerializer, LeagueDetailSerializer, GroupSerializer, \
    GroupDetailSerializer, SubGroupSerializer, TeamSerializer, KnockoutGroupSerializer, KnockoutSerializer, \
    MatchDaySerializer, FixtureSerializer, TableRowSerializer


class SeasonsViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer


class LeaguesViewSet(NestedViewSetMixin, DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    serializer_detail_class = LeagueDetailSerializer
    filter_class = LeaguesFilter


class GroupsViewSet(NestedViewSetMixin, DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    serializer_detail_class = GroupDetailSerializer
    filter_class = GroupsFilter


class KnockoutGroupsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = KnockoutGroup.objects.all()
    serializer_class = KnockoutGroupSerializer


class SubGroupsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubGroup.objects.all()
    serializer_class = SubGroupSerializer
    filter_class = SubGroupsFilter


class TeamsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class KnockoutsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Knockout.objects.all()
    serializer_class = KnockoutSerializer


class MatchDaysViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MatchDay.objects.all()
    serializer_class = MatchDaySerializer


class FixturesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Fixture.objects.all()
    serializer_class = FixtureSerializer


class TableRowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TableRow.objects.all()
    serializer_class = TableRowSerializer
