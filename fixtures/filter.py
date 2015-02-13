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
