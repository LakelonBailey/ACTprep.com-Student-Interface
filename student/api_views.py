from django.http import HttpResponse
from django.shortcuts import render, redirect
from student.models import DailyStatCollection
from student.modules.studentTasks import *
from datetime import datetime
from .forms import CategoryForm, DailyStatForm, LessonForm, TestForm, ChallengeForm
from actprep.settings import BASE_DIR
import os
import csv


def check_in(request):
    can_check_in = validateCheckInTime()
    if can_check_in:
        stats = getStatCollection(request.user)
        stats.did_check_in = True
        stats.save()
    return redirect('/student/dashboard')


def add_csv_data(request):
    file = 'Challenges.csv'
    file_path = os.path.join(BASE_DIR, 'student/data/' + file)
    file = open(file_path)
    data = csv.reader(file)
    header = next(data)
    objArr = []

    for row in data:
        memDayObj = {}
        for i in range(len(row)):
            memDayObj[header[i]] = row[i]
        objArr.append(memDayObj)
    return HttpResponse(200)


def input_stats(request):
    form = DailyStatForm(request.POST)
    if form.is_valid():
        weekday = datetime.today().weekday()

        data = form.cleaned_data
        hours_worked = float(data['hours_worked'])
        memorization_time = data['memorization_time']
        practice_quiz_score = data['practice_quiz_score']

        stat_collection = DailyStatCollection.objects.get(user=request.user, day=weekday)
        stat_collection.hours_worked = hours_worked
        stat_collection.memorization_time = memorization_time
        stat_collection.practice_quiz_score = practice_quiz_score
        stat_collection.save()
    else:
        print('invalid')
    return redirect('/student/dashboard')


def new_test(request):
    user = request.user
    form = TestForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        addNewTest(data, user)
    else:
        print(form.errors)

    return redirect('/student/dashboard')


def new_challenge(request):
    user = request.user
    form = ChallengeForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        addNewChallenge(data, user)
    else:
        print(form.errors)
    
    return redirect('/student/dashboard')


def new_category(request):
    user = request.user
    form = CategoryForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        addNewCategory(data, user)
    else:
        return HttpResponse(form.errors)

    return redirect('/student/dashboard')


def new_lesson(request):
    user = request.user
    form = LessonForm(request.POST)

    if form.is_valid():
        data = form.cleaned_data
        addNewLesson(data, user)
    else:
        return HttpResponse(form.errors)

    return redirect('/student/dashboard')
