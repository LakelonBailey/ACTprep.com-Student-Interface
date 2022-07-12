from student.models import LessonDone, CategoryDone, Challenge, ChallengeDone, StudentProfile, StudentWeek, Test, DailyStatCollection, TestDone
from datetime import datetime, timedelta


def verifyStudent(user):
    if user.groups.filter(name='Student').exists():
        student = StudentProfile.objects.get(user=user)
        return student
    else:
        return False


def parseWeekString(week):
    week_arr = week.split('_')
    week = week_arr[0].capitalize() + ' Week ' + week_arr[1]
    return week


def addTest(arr):
    for test in arr:
        test = Test.objects.create(
            name=test['name'],
            test_location=test['test_location'],

            english_order=test['english_order'],
            english_location=test['english_location'],
            english_answers=test['english_answers'],

            math_order=test['math_order'],
            math_location=test['math_location'],
            math_answers=test['math_answers'],

            reading_order=test['reading_order'],
            reading_location=test['reading_location'],
            reading_answers=test['reading_answers'],

            science_order=test['science_order'],
            science_location=test['science_location'],
            science_answers=test['science_answers'],

            conversion_chart_link=test['conversion_chart_link'],
            full_test_order=test['full_test_order']
        )
        test.save()


def addChallenge(arr):
    for chal in arr:
        test = Test.objects.get(name = chal['test'])
        challenge = Challenge.objects.create(
            subject = chal['subject'],
            order = int(chal['order']),
            test = test,
            questions_to_do = chal['questions_to_do'],
            time_allowed = float(chal['time_allowed']),
            total_questions = int(chal['total_questions'])
        )
        challenge.save()


def getStatCollection(user):
    today = datetime.today() - timedelta(hours=4)
    today = today.date()
    weekday = today.weekday()
    stat_collection = DailyStatCollection.objects.filter(day = weekday, user=user)
    if stat_collection.exists():
        stat_collection = stat_collection[0]
    else:
        week = StudentWeek.objects.get(user=user, start_date__lte=today, end_date__gte=today)
        stat_collection = DailyStatCollection.objects.create(
            user=user,
            week=week,
            day=weekday
        )
        stat_collection.save()
    return stat_collection
        

def addNewTest(data, user):
    test = data['test']

    testDone = TestDone.objects.filter(test=test, user=user)
    if testDone.exists():
        testDone = testDone[0]

        testDone.english_tried = data['english_tried']
        testDone.english_correct = data['english_correct']
        testDone.english_score = data['english_score']
        testDone.math_tried = data['math_tried']
        testDone.math_correct = data['math_correct']
        testDone.math_score = data['math_score']
        testDone.reading_tried = data['reading_tried']
        testDone.reading_correct = data['reading_correct']
        testDone.reading_score = data['reading_score']
        testDone.science_tried = data['science_tried']
        testDone.science_correct = data['science_correct']
        testDone.science_score = data['science_score']
        testDone.save()
    else:
        testDone = TestDone.objects.create(
            user=user,
            day=getStatCollection(user),
            test=test,
            was_challenge_test=False,
            english_tried=data['english_tried'],
            english_correct=data['english_correct'],
            english_score=data['english_score'],
            math_tried=data['math_tried'],
            math_correct=data['math_correct'],
            math_score=data['math_score'],
            reading_tried=data['reading_tried'],
            reading_correct=data['reading_correct'],
            reading_score=data['reading_score'],
            science_tried=data['science_tried'],
            science_correct=data['science_correct'],
            science_score=data['science_score']
        )
        testDone.save()

def addNewChallenge(data, user):
    challenge = data['challenge']
    total_correct = data['total_correct']

    challengeDone = ChallengeDone.objects.filter(user=user, challenge=challenge)

    if challengeDone.exists():
        challengeDone = challengeDone[0]
        challengeDone.total_correct = total_correct
        challengeDone.save()
    else:
        challengeDone = ChallengeDone.objects.create(
            user=user,
            day=getStatCollection(user),
            challenge=challenge,
            total_correct=total_correct
        )
        challengeDone.save()


def addNewCategory(data, user):
    category = data['category']
    time_spent = data['time_spent']

    categoryDone = CategoryDone.objects.filter(user=user, category=category)

    if categoryDone.exists():
        categoryDone = categoryDone[0]
        categoryDone.time_spent = time_spent
        categoryDone.save()
    else:
        categoryDone = CategoryDone.objects.create(
            user=user,
            day=getStatCollection(user),
            category=category,
            time_spent=time_spent
        )


def addNewLesson(data, user):
    lesson = data['lesson']
    time_spent = data['time_spent']

    lessonDone = LessonDone.objects.filter(user=user,lesson=lesson)

    if lessonDone.exists():
        lessonDone = lessonDone[0]
        lessonDone.time_spent = time_spent
        lessonDone.save()
    else:
        lessonDone = LessonDone.objects.create(
            user=user,
            day=getStatCollection(user),
            lesson=lesson,
            time_spent=time_spent
        )
        lessonDone.save()


def validateCheckInTime():
    time = datetime.now() - timedelta(hours=4)
    time = time.hour
    if time >= 12 or time < 6:
        return False
    else:
        return True
