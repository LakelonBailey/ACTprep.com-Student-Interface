from django.http import HttpResponse
from django.shortcuts import render, redirect
from student.models import ChallengeDone, TestDone, Category, Challenge, Lesson
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from student.modules.studentTasks import *
from pprint import PrettyPrinter
from .forms import TestForm

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
        student = StudentProfile.objects.get(user=user)
        stat_collection = getStatCollection(user)

        tests_taken = TestDone.objects.filter(day=stat_collection)
        challenges_taken = ChallengeDone.objects.filter(day=stat_collection)
        categories_done = CategoryDone.objects.filter(day=stat_collection)
        lessons_done = LessonDone.objects.filter(day=stat_collection)

        mem_info = stat_collection.week.memorization_week
        week = parseWeekString(mem_info.week)

        subject = mem_info.week.split('_')[0]
        success_calc = getSuccessCalculations(student)

        test_form = TestForm()
        challenges = Challenge.objects.filter(subject=subject)
        categories = Category.objects.filter(subject=subject)
        lessons = Lesson.objects.filter(subject=subject)

        context = {
            'student': student,
            'stats': stat_collection,
            'mem_info': mem_info,
            'week': week,
            'test_form': test_form,
            'tests_taken': tests_taken,
            'challenges': challenges,
            'categories': categories,
            'challenges_taken': challenges_taken,
            'categories_done': categories_done,
            'lessons': lessons,
            'lessons_done': lessons_done,
            'success_calc': success_calc
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
