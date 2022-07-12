from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'math/index.html')

def instructions(request):
    return render(request, 'math/instructions.html')

def lessons(request):
    return HttpResponse('You are at the Math Lessons Page')