from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import render, get_object_or_404

import pytz

from .models import *
from .generatehtml import *

def index(request):
    launches = Launch.objects.order_by("-time")
    template = loader.get_template("launches/index.html")
    context = {"launches": launches}

    return render(request, "launches/index.html", context)

def home(request):
    return HttpResponse("Hello, Django!")


def launch_details(request, launch_name):
    launch = get_object_or_404(Launch, name=launch_name)
    return HttpResponse(create_launch_table(launch))
