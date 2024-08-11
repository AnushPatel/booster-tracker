from django.shortcuts import HttpResponse


def health(request):
    return HttpResponse("Success", status=200)
