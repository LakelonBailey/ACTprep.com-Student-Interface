from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'reading/index.html')

def instructions(request):
    return render(request, 'reading/instructions.html')

def lessons(request):
    return HttpResponse('You are at the Reading Lessons Page')