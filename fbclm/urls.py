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
