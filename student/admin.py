from django.contrib import admin
from .models import *


def register_list(modelList):
    for model in modelList:
        admin.site.register(model)


modelList = [
    StudentProfile,
    StudentWeek,
    DailyStatCollection,
    Test,
    ProgramDay,
    TestDone,
    Challenge,
    ChallengeDone,
    CategoryGroup,
    Category,
    CategoryDone,
    Lesson,
    LessonDone
    ]

register_list(modelList)
