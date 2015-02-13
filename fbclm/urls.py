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

from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework_extensions.routers import ExtendedDefaultRouter

from fixtures import views


router = ExtendedDefaultRouter()
router.register(r'seasons', views.SeasonsViewSet) \
    .register(r'leagues',
              views.LeaguesViewSet,
              base_name='season-league',
              parents_query_lookups=['season']) \
    .register(r'groups',
              views.GroupsViewSet,
              base_name='league-group',
              parents_query_lookups=['league__season', 'league'])

router.register(r'leagues', views.LeaguesViewSet)
router.register(r'groups', views.GroupsViewSet)
router.register(r'knockout_groups', views.KnockoutGroupsViewSet)
router.register(r'subgroups', views.SubGroupsViewSet)
router.register(r'teams', views.TeamsViewSet)
router.register(r'knockouts', views.KnockoutsViewSet)
router.register(r'matchdays', views.MatchDaysViewSet)
router.register(r'fixtures', views.FixturesViewSet)
router.register(r'tables', views.TableRowViewSet)

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       url(r'^admin/', include(admin.site.urls)), )
