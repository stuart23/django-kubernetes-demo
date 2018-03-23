from django.conf import settings
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

from .models import Message
from .tasks import hasher

from django.core.cache import cache

import math
import socket
import logging

logger = logging.getLogger('django')


def _update_visited():
    """ Updates the visited count by one in the cache
    :return: The visited count in string form.
    """
    visited = cache.get('visited')
    if not visited:
        visited = 0
    else:
        visited = int(visited)
    visited += 1
    cache.set('visited', str(visited))
    return str(visited)


def index(request):
    """ Updates the visited count and provides the static URL to build the main
     landing page.
    """

    visited = _update_visited()
    context = {
                 "STATIC_URL": settings.STATIC_URL,
                 "visited": visited,
                 "pod_name": socket.gethostname()
               }
    return render(request, 'index.html', context)


def messages(request):
    """ REST endpoint providing basic operations. GET will return the list of
    all messages created so far in JSON form, POST will add a new message to
    the list of messages (guestbook).
    """
    if request.method == 'GET':
        data = serializers.serialize("json", Message.objects.all())
        return HttpResponse(data)
    elif request.method == 'POST':
        message = Message.objects.create(text=request.body)
        hasher.delay(message.pk)
        return HttpResponse(request.body)
    else:
        return HttpResponse("Unsupported HTTP Verb.")


def compute(request):
    """ Endpoint that does some CPU intensive work to help demonstrate
     autoscaling.
    """
    logging.info("doing some long calculations")
    x = 0.0001
    for i in range(0, 1000000):
        x += math.sqrt(x)
    return HttpResponse("Performed a lot of work")
