from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'science/index.html')

def instructions(request):
    return render(request, 'science/instructions.html')

def lessons(request):
    return HttpResponse('You are at the Science Lessons Page')