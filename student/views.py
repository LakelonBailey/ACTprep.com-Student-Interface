from django.http import HttpResponse
from django.shortcuts import render, redirect
from student.models import ChallengeDone, TestDone
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from student.modules.studentTasks import *
from pprint import PrettyPrinter
from .forms import CategoryForm, LessonForm, TestForm, ChallengeForm

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

        can_check_in = validateCheckInTime()

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
            'lessons_done': lessons_done,
            'can_check_in': can_check_in
        }

        return render(request, 'dashboard.html', context)
    else:
        return(HttpResponse(200))


@login_required
def contact(request):
    return render(request, 'contact.html')


@login_required
def logout(request):
    auth_logout(request)
    return redirect('/accounts/login')
