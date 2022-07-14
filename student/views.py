from django.http import HttpResponse
from django.shortcuts import render, redirect
from student.models import ChallengeDone, TestDone, Category, Challenge, Lesson
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from student.modules.studentTasks import *
from pprint import PrettyPrinter
from .forms import ChallengeForm, TestForm

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
        success_calc = getSuccessCalculations(student)
        day = parseDayString(stat_collection.program_day.day)

        subject = stat_collection.program_day.day.split('_')[0]

        categories = Category.objects.filter(subject=subject)
        challenges = Challenge.objects.filter(subject=subject)
        lessons = Lesson.objects.filter(subject=subject)
        tests = Test.objects.all()

        context = {
            'student': student,
            'stats': stat_collection,
            'tests': tests,
            'tests_taken': tests_taken,
            'challenges_taken': challenges_taken,
            'categories_done': categories_done,
            'lessons_done': lessons_done,
            'success_calc': success_calc,
            'program_day': stat_collection.program_day,
            'day': day,
            'schedule': stat_collection.program_day.schedule,
            'categories': categories,
            'lessons': lessons,
            'challenges': challenges
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
