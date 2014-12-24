# coding=utf-8
import urllib
import urllib2
from datetime import datetime

from bs4 import BeautifulSoup
from django.db.transaction import atomic
import pytz

from models import Season, League, Group, SubGroup, MatchDay, Team, Fixture, Knockout, KnockoutGroup


FIXTURES_URL = 'http://www.fbclm.net/dinamico/competiciones/competiciones.asp'

# Parser tags
NAME_ATTRIBUTE = 'name'
SELECTORS_HTML_TAG = 'table'
VALUE_ATTR = 'value'
DATE_FORMAT_SHORT_YEAR = '%d/%m/%y %H:%Mh'
DATE_FORMAT_FULL_YEAR = '%d/%m/%Y %H:%Mh'
DATE_FORMAT_MATCH_DAY = '%d/%m/%Y'
TBODY_TAG = 'tbody'

# Headers
ACCEPT_ENCODING = 'Accept-Encoding'
ENCODING = 'gzip, deflate'
ACCEPT_LANGUAGE = 'Accept-Language'
LANGUAGE = 'en,en-US;q=0.8,es;q=0.6'
CACHE_CONTROL = 'Cache-Control'
CACHE = 'max-age=0'
CONNECTION = 'Connection'
KEEP_ALIVE = 'keep-alive'
CONTENT_TYPE = 'Content-Type'
X_WWW_FORM = 'application/x-www-form-urlencoded'
COOKIE = 'Cookie'
COOKIE_VALUE = 'ASPSESSIONIDQCTBBBCC=BEHNECLDNOFKEEIIPKIADEID; ASPSESSIONIDQCRCCBCB=KBEBFPHAGCGJPOBNENOGIACM'
HOST = 'Host'
HOST_VALUE = 'www.fbclm.net'
ORIGIN = 'Origin'
ORIGIN_VALUE = 'http://www.fbclm.net'
REFERER = 'Referer'

# Form parameters
LOGIN = 'login'
PASS = 'pass'
NEWS_ID = 'id_noticia'
NEWS_TYPE_ID = 'id_tipo_noticia'
MATCH_ID = 'id_partido'
ONLINE = 'online'
SEASON_ID = 'id_temporada'
LEAGUE_ID = 'agrupacion'
CATEGORY_ID = 'id_categoria'
GROUP_ID = 'id_grupo'
MATCH_DAY_ID = 'id_jornada'


def parse_html():
    """
    Parse all fixtures from html
    """

    content = urllib2.urlopen(FIXTURES_URL).read()
    parsed_html = BeautifulSoup(content)
    selectors_html = parsed_html.find(SELECTORS_HTML_TAG)
    seasons_html = selectors_html.find(attrs={NAME_ATTRIBUTE: SEASON_ID})

    print parse_seasons(seasons_html)


@atomic
def parse_seasons(seasons_html):
    """

    :param seasons_html:
    :return:
    """
    for season_html in seasons_html:
        season_id = season_html[VALUE_ATTR]
        season_name = season_html.string

        season = Season.objects.update_or_create(season_name=season_name)[0]

        if season_id == '20':
            parse_leagues(season, season_id)

        if season.league_set.count() == 0:
            season.delete()


def parse_leagues(season, season_id):
    season_html = request_seasons_html(season_id=season_id)
    leagues_html = season_html.find(attrs={NAME_ATTRIBUTE: LEAGUE_ID})

    for league_html in leagues_html.contents[1:]:
        league_name = league_html.string

        league_id = league_html[VALUE_ATTR]
        league_name = unicode(league_name)

        league = League.objects.update_or_create(name=league_name, season=season)[0]

        parse_groups(season_id, league, league_id)


def parse_groups(season_id, league, league_id):
    league_html = request_league_html(season_id=season_id, league_id=league_id)
    groups_html = league_html.find(attrs={NAME_ATTRIBUTE: GROUP_ID})

    if len(groups_html.contents) > 1:
        create_group(season_id, league, league_id, groups_html, False)
    else:
        groups_html = league_html.find(attrs={NAME_ATTRIBUTE: CATEGORY_ID})
        create_group(season_id, league, league_id, groups_html, True)


def create_group(season_id, league, league_id, groups_html, has_subgroups):
    for group_html in groups_html.contents[1:]:
        group_id = group_html[VALUE_ATTR]
        group_name = unicode(group_html.string)

        if group_name == 'COPA PRESIDENTE' or group_name == 'COPA FEDERACION':
            group = KnockoutGroup.objects.update_or_create(name=group_name, league=league)[0]
            parse_knockout(season_id, league, league_id, group, group_id)
            return

        group = Group.objects.update_or_create(name=group_name, league=league)[0]

        if not has_subgroups and not group_name.__contains__('FASE FINAL') and not (
                        league.name == 'JUNIOR MASCULINO ESPECIAL' and group_name.__contains__('FASE')) \
                and not group_name == 'PLAY OFF ASCENSO 1/4 FINAL' \
                and not group_name == 'GRUPO ESTE - PLAY OFF' \
                and not group_name.__contains__('COPA PRESIDENTE') \
                and not group_name == 'COPA FEDERACION' \
                and not group_name == 'COPA IGUALDAD' \
                and not group_name == 'ESTE FASE 3 CRUCES' \
                and not group_name == 'CRUCES' \
                and not group_name == 'CRUCES 1 AL 4' \
                and not group_name == '1/4 FINAL' \
                and not group_name == 'COPA ADECCO PLATA' \
                and not group_name == 'FINAL A CUATRO' \
                and not group_name == 'COPA ADECCO BRONCE' \
                and not group_name.__contains__('TROFEO JCCM') \
                and not group_name.__contains__('CRUCES 0') \
                and not group_name == 'SERIES' \
                and not group_name.__contains__('ELIMINATORIAS') \
                and not group_name == 'FINAL' \
                and not group_name.__contains__('ASCENSO') \
                and not group_name.__contains__('PLAY-OFF') \
                and not group_name == 'FASE 2' \
                and not group_name == 'COPA PRIMAVERA FASE 1' \
                and not group_name == 'CUARTOS DE FINAL' \
                and not group_name.__contains__('MASCULINO 1') \
                and not group_name.__contains__('MASCULINO 5') \
                and not group_name == 'FASE DE CLASIFICACION' \
                and not league.name == 'SUPERCOPA F.B.C.M.' \
                and not group_name.__contains__('COPA 2') \
                and not group_name.__contains__('ALCAZAR DE SAN JUAN MASCULINO 3') \
                and not group_name.__contains__('ALCAZAR DE SAN JUAN MASCULINO 5') \
                and not group_name == 'ALCAZAR DE SAN JUAN MASCULINO FINAL':
            parse_match_day(season_id, league, league_id, group, group_id)
        else:
            parse_subgroups(season_id, league, league_id, group, group_id)


def parse_subgroups(season_id, league, league_id, group, group_id):
    group_html = request_area_html(season_id, league_id, group_id)
    subgroups_html = group_html.find(attrs={NAME_ATTRIBUTE: GROUP_ID})
    for subgroup_html in subgroups_html.contents[1:]:
        subgroup_id = subgroup_html[VALUE_ATTR]
        subgroup_name = unicode(subgroup_html.string)

        subgroup = SubGroup.objects.update_or_create(name=subgroup_name, group=group)[0]

        parse_subgroup_match_day(season_id, league, league_id, group_id, subgroup, subgroup_id)


def parse_match_day(season_id, league, league_id, group, group_id):
    group_html = request_web_page(season_id, league_id, 0, group_id, 0)
    match_days_html = group_html.find(attrs={NAME_ATTRIBUTE: MATCH_DAY_ID})

    for match_day_html in match_days_html.contents[1:]:
        match_day_id = match_day_html[VALUE_ATTR]
        match_day_name = unicode(match_day_html.string)
        match_day_name = match_day_name.split()[1][1:-1]
        match_day_name = datetime.strptime(match_day_name, DATE_FORMAT_MATCH_DAY).replace(tzinfo=pytz.utc)

        match_day = MatchDay.objects.update_or_create(date=match_day_name, group=group)[0]

        parse_fixtures(season_id, league, league_id, group_id, match_day_id, match_day)


def parse_subgroup_match_day(season_id, league, league_id, category_id, subgroup, subgroup_id):
    subgroup_html = request_web_page(season_id, league_id, category_id, subgroup_id, 0)
    match_days_html = subgroup_html.find(attrs={NAME_ATTRIBUTE: MATCH_DAY_ID})

    for match_day_html in match_days_html.contents[1:]:
        match_day_id = match_day_html[VALUE_ATTR]
        match_day_name = unicode(match_day_html.string)
        match_day_name = match_day_name.split()[1][1:-1]
        match_day_name = datetime.strptime(match_day_name, DATE_FORMAT_MATCH_DAY).replace(tzinfo=pytz.utc)

        match_day = MatchDay.objects.update_or_create(date=match_day_name, subgroup=subgroup)[0]

        parse_subgroup_fixtures(season_id, league, league_id, category_id, subgroup_id, match_day_id, match_day)


def parse_fixtures(season_id, league, league_id, group_id, match_day_id, match_day):
    fixtures_rows = list(request_web_page(season_id, league_id, 0, group_id, match_day_id).find(TBODY_TAG).children)
    fixtures_rows = list(fixtures_rows[8].find(TBODY_TAG).children)[1::2]

    for fixture_html in fixtures_rows:
        fixture_html = list(fixture_html.children)[1:]
        date_strings = list(fixture_html[0].strings)
        score_strings = list(fixture_html[1].strings)
        teams_strings = list(fixture_html[2].strings)

        date = None

        # Date isn't 'Aplazado'
        if len(date_strings) == 2:
            date = datetime.strptime(date_strings[0] + ' ' + date_strings[1], DATE_FORMAT_SHORT_YEAR).replace(
                tzinfo=pytz.utc)

        # Score is '--'
        if len(score_strings) == 1:
            score_strings = [0, 0]

        home_team = Team.objects.update_or_create(name=unicode(teams_strings[0]), league=league)[0]
        away_team = Team.objects.update_or_create(name=unicode(teams_strings[1]), league=league)[0]

        Fixture.objects.update_or_create(match_day=match_day, home_team=home_team,
                                         home_score=score_strings[0], away_team=away_team,
                                         away_score=score_strings[1], date=date)


def parse_subgroup_fixtures(season_id, league, league_id, category_id, subgroup_id, match_day_id, match_day):
    fixtures_rows = list(
        request_web_page(season_id, league_id, category_id, subgroup_id, match_day_id).find(TBODY_TAG).children)
    fixtures_rows = list(fixtures_rows[8].find(TBODY_TAG).children)[1::2]

    for fixture_html in fixtures_rows:
        fixture_html = list(fixture_html.children)[1:]
        date_strings = list(fixture_html[0].strings)
        score_strings = list(fixture_html[1].strings)
        teams_strings = list(fixture_html[2].strings)

        date = None

        # Date isn't 'Aplazado'
        if len(date_strings) == 2:
            if date_strings[1] == 'Sin Hora':
                date_strings[1] = '00:00h'
            else:
                time = date_strings[1]
                # 2014/2015 -> Alevin Masculino -> Ciudad Real -> Grupo F -> Jornada 3
                if not ':' in time and not '-' in time:
                    date_strings[1] = time[:2] + ':' + time[2:]
                else:
                    # 2014/2015 -> Alevin Femenino -> AF-02-B TOLEDO-TALAVERA-TORRIJOS -> Jornada 2
                    if match_day_id == '13853':
                        if time[4] == 'h':
                            time = time[:4]
                        score_strings = [time[:2], time[3:5]]
                        date_strings[1] = '00:00h'

            date = datetime.strptime(date_strings[0] + ' ' + date_strings[1], DATE_FORMAT_SHORT_YEAR).replace(
                tzinfo=pytz.utc)

        # Score is '--'
        if len(score_strings) == 1:
            score_strings = [0, 0]

        home_team = Team.objects.update_or_create(name=unicode(teams_strings[0]), league=league)[0]
        away_team = Team.objects.update_or_create(name=unicode(teams_strings[1]), league=league)[0]

        Fixture.objects.update_or_create(match_day=match_day, home_team=home_team,
                                         home_score=score_strings[0], away_team=away_team,
                                         away_score=score_strings[1], date=date)


def parse_knockout(season_id, league, league_id, group, group_id):
    rows = list(request_web_page(season_id, league_id, 0, group_id, 0).find(TBODY_TAG).children)

    venue = rows[6].next.next.next.next[6:]
    group.venue = venue
    group.save()

    knockouts_html = rows[8:]
    knockout_index = 0
    knockout = None

    for knockout_html in knockouts_html:
        if knockout_index % 2 == 0:
            knockout_name = knockout_html.next.text.split()[0]
            knockout = Knockout.objects.update_or_create(group=group, stage=knockout_name)[0]
        else:
            fixtures_html = list(knockout_html.find(TBODY_TAG).children)[2::2]

            for fixture_html in fixtures_html:
                fixture_html = list(fixture_html.children)[2:5]
                date_strings = list(fixture_html[0].strings)
                date = datetime.strptime(date_strings[0] + ' ' + date_strings[1], DATE_FORMAT_FULL_YEAR).replace(
                    tzinfo=pytz.utc)

                score_strings = list(fixture_html[1].strings)
                teams_strings = list(fixture_html[2].strings)

                home_team = Team.objects.update_or_create(name=teams_strings[0], league=league)[0]
                away_team = Team.objects.update_or_create(name=teams_strings[1], league=league)[0]

                Fixture.objects.update_or_create(knockout=knockout, home_team=home_team,
                                                 home_score=score_strings[0], away_team=away_team,
                                                 away_score=score_strings[1], date=date)

        knockout_index += 1


def request_seasons_html(season_id):
    return request_web_page(season_id=season_id, league_id=0, category_id=0, group_id=0, match_day_id=0)


def request_league_html(season_id, league_id):
    return request_web_page(season_id=season_id, league_id=league_id, category_id=0, group_id=0, match_day_id=0)


def request_area_html(season_id, league_id, category_id):
    return request_web_page(season_id=season_id, league_id=league_id, category_id=category_id, group_id=0,
                            match_day_id=0)


def request_group_html(season_id, league_id, group_id):
    return request_web_page(season_id=season_id, league_id=league_id, category_id=0, group_id=group_id, match_day_id=0)


def request_web_page(season_id, league_id, category_id, group_id, match_day_id):
    headers = {ACCEPT_ENCODING: ENCODING,
               ACCEPT_LANGUAGE: LANGUAGE,
               CACHE_CONTROL: CACHE,
               CONNECTION: KEEP_ALIVE,
               CONTENT_TYPE: X_WWW_FORM,
               COOKIE: COOKIE_VALUE,
               HOST: HOST_VALUE,
               ORIGIN: ORIGIN_VALUE,
               REFERER: FIXTURES_URL}

    values = {LOGIN: '',
              PASS: '',
              NEWS_ID: 0,
              NEWS_TYPE_ID: 0,
              MATCH_ID: 0,
              ONLINE: 1,
              SEASON_ID: season_id,
              LEAGUE_ID: league_id,
              CATEGORY_ID: category_id,
              GROUP_ID: group_id,
              MATCH_DAY_ID: match_day_id}

    data = urllib.urlencode(values)
    request = urllib2.Request(FIXTURES_URL, data, headers)
    response = urllib2.urlopen(request)
    return BeautifulSoup(response.read(), "html5lib")