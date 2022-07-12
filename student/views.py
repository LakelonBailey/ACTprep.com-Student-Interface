from django.http import HttpResponse
from django.shortcuts import render, redirect
from student.models import ChallengeDone, DailyStatCollection, StudentProfile, Test, TestDone
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from student.modules.studentTasks import *
from actprep.settings import BASE_DIR
import os
import csv
from pprint import PrettyPrinter
from datetime import datetime
from .forms import CategoryForm, DailyStatForm, LessonForm, TestForm, ChallengeForm

pp = PrettyPrinter(indent=2)

weekDays = ['Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday'
            ]


@login_required
def index(request):
    user = request.user
    student = verifyStudent(user)
    if student:
        return redirect('dashboard/')
    else:
        return HttpResponse('Not a student')


@login_required
def dashboard(request):
    if request.method == 'GET':
        user = request.user
        stat_collection = getStatCollection(user)
        tests_taken = TestDone.objects.filter(day=stat_collection)
        challenges_taken = ChallengeDone.objects.filter(day=stat_collection)
        categories_done = CategoryDone.objects.filter(day=stat_collection)
        lessons_done = LessonDone.objects.filter(day=stat_collection)
        mem_info = stat_collection.week.memorization_week
        week = parseWeekString(mem_info.week)
        
        test_form = TestForm()
        challenge_form = ChallengeForm()
        category_form = CategoryForm()
        lesson_form = LessonForm()

        context = {
            'stats': stat_collection,
            'mem_info': mem_info,
            'week': week,
            'test_form': test_form,
            'tests_taken': tests_taken,
            'challenge_form': challenge_form,
            'challenges_taken': challenges_taken,
            'category_form': category_form,
            'categories_done': categories_done,
            'lesson_form': lesson_form,
            'lessons_done': lessons_done
        }

        return render(request, 'dashboard.html', context)
    else:
        return(HttpResponse(200))


def add_data(request):
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


# Contact page will gather determine student's coach(es) and display only
# their contact information
@login_required
def contact(request):
    return render(request, 'contact.html')


# Logout view will log out the user and then provide a success page that
# links the Login Page in case students want to log back in.
@login_required
def logout(request):
    auth_logout(request)
    return redirect('/accounts/login')
