# from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse  # HttpResponseRedirect
# from django.core.urlresolvers import reverse
# from django.views import generic
# from django.utils import timezone


def index(request):
    return HttpResponse("'Anderson, don’t talk out loud. You lower the " +
                        "IQ of the whole street.'-Sherlock")
