from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'english/index.html')


def instructions(request):
    return render(request, 'english/instructions.html')


def lessons(request):
    return HttpResponse('You are at the English Lessons Page')
