from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("'Anderson, don’t talk out loud. You lower the "
                        "IQ of the whole street.'-Sherlock")
