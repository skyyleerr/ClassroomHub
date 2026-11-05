from django.http import HttpResponse


def home(request):
    return HttpResponse("Welcome to ClassroomHub")


def resources(request):
    return HttpResponse("Learning resources")


def about(request):
    return HttpResponse("About ClassroomHub")
