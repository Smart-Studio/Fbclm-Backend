from django.http import HttpResponse

from parser import parse_html


def index(request):
    parse_html()
    return HttpResponse("Hello, world. You're at the polls index.")