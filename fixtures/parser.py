import urllib2

from bs4 import BeautifulSoup

from models import Season

NAME_ATTRIBUTE = 'name'
FIXTURES_URL = 'http://www.fbclm.net/dinamico/competiciones/competiciones.asp'
SELECTORS_HTML_TAG = 'table'
SEASON_ID = 'id_temporada'


def parse_fixtures():
    content = urllib2.urlopen(FIXTURES_URL).read()
    soup = BeautifulSoup(content)
    selectors_html = soup.find(SELECTORS_HTML_TAG)
    seasons_html = selectors_html.find(attrs={NAME_ATTRIBUTE: SEASON_ID})

    for season_html in seasons_html:
        season = Season(season_name=season_html.string)
        print season
