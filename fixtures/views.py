from django.http import HttpResponse

from parser import parse_fixtures


def index(request):
    parse_fixtures()
    return HttpResponse("Hello, world. You're at the polls index.")