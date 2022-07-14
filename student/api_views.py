from django.http import HttpResponse
from django.shortcuts import redirect
from student.models import DailyStatCollection
from student.modules.studentTasks import *
from datetime import datetime
from .forms import CategoryForm, DailyStatForm, LessonForm, TestForm, ChallengeForm
from actprep.settings import BASE_DIR
import os
import csv
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=2)


def check_in(request):
    can_check_in = validateCheckInTime()
    stats = getStatCollection(request.user)
    if can_check_in:
        stats.did_check_in_before_noon = True
        stats.did_check_in = True
        stats.save()
    else:
        stats.did_check_in = True
        stats.did_check_in_before_noon = False
        stats.save()
    return redirect('/student/dashboard')


def add_csv_data(request):
    file = 'ProgramDay.csv'
    file_path = os.path.join(BASE_DIR, 'student/data/' + file)
    file = open(file_path)
    data = csv.reader(file)
    header = next(data)
    objArr = []

    for row in data:
        obj = {}
        for i in range(len(row)):
            obj[header[i]] = row[i]
        objArr.append(obj)

    schedule_items = []
    for item in objArr:
        for x in item['schedule'].split('_'):
            if not x in schedule_items:
                schedule_items.append(x)
    return HttpResponse(pp.pformat(schedule_items))


def input_stats(request):
    form = DailyStatForm(request.POST)
    if form.is_valid():
        today = datetime.today()

        data = form.cleaned_data
        hours_worked = float(data['hours_worked'])
        memorization_time = data['memorization_time']
        practice_quiz_score = data['practice_quiz_score']

        stat_collection = DailyStatCollection.objects.get(user=request.user, date=today)
        stat_collection.hours_worked = hours_worked
        stat_collection.memorization_time = memorization_time
        stat_collection.practice_quiz_score = practice_quiz_score
        stat_collection.did_check_in = True
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
