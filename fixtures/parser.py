import urllib
import urllib2

from bs4 import BeautifulSoup

from models import Season, League


FIXTURES_URL = 'http://www.fbclm.net/dinamico/competiciones/competiciones.asp'

# Parser tags
NAME_ATTRIBUTE = 'name'
SELECTORS_HTML_TAG = 'table'
VALUE_ATTR = 'value'

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
CATEGORY_ID = 'categoria'
GROUP_ID = 'id_grupo'
MATCH_DAY_ID = 'id_jornada'


def parse_fixtures():
    content = urllib2.urlopen(FIXTURES_URL).read()
    parsed_html = BeautifulSoup(content)
    selectors_html = parsed_html.find(SELECTORS_HTML_TAG)
    seasons_html = selectors_html.find(attrs={NAME_ATTRIBUTE: SEASON_ID})

    print parse_seasons(seasons_html)


def parse_seasons(seasons_html):

    for season_html in seasons_html:
        season_id = season_html[VALUE_ATTR]
        season_name = season_html.string
        season = Season.objects.filter(season_name=season_name)

        if season.exists():
            season = season[0]
        else:
            season = Season(season_name=season_html.string)
            season.save()

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
                  LEAGUE_ID: 0,
                  CATEGORY_ID: 0,
                  GROUP_ID: 0,
                  MATCH_DAY_ID: 0}

        data = urllib.urlencode(values)
        request = urllib2.Request(FIXTURES_URL, data, headers)
        response = urllib2.urlopen(request)
        html = BeautifulSoup(response.read())

        parse_leagues(season, html)

        if season.league_set.count() == 0:
            season.delete()


def parse_leagues(season, season_html):
    leagues_html = season_html.find(attrs={NAME_ATTRIBUTE: LEAGUE_ID})
    for league_html in leagues_html:
        league_name = league_html.string
        if league_name:
            league_name = unicode(league_name)
            league = League.objects.filter(name=league_name, season=season.id)

            if not league.exists():
                season.league_set.create(name=league_name)
