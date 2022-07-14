from math import ceil as roundup
from student.models import *
from datetime import datetime, timedelta


def verifyStudent(user):
    if user.groups.filter(name='Student').exists():
        student = StudentProfile.objects.get(user=user)
        return student
    else:
        return False


def parseDayString(day):
    day_arr = day.split('_')
    day = day_arr[0].capitalize() + ' Week ' + day_arr[1] + ' Day ' + day_arr[2]
    return day


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


def addProgramDay(arr):
    for day in arr:
        schedule = day['schedule'].split('_')
        ProgramDay.objects.create(
            day=day['day'],
            memorization_link=day['memorization_link'],
            answer_sheet=day['answer_sheet'],
            quizlet=day['quizlet'],
            extra_practice=day['extra_practice'],
            practice_quiz_link=day['practice_quiz_link'],
            video_link=day['video_link'],
            in_class_quiz=day['in_class_quiz'],
            schedule=schedule
        )


def getStatCollection(user):
    today = datetime.today() - timedelta(hours=4)
    today = today.date()
    week = StudentWeek.objects.get(user=user, start_date__lte=today, end_date__gte=today)

    week_stats = DailyStatCollection.objects.filter(user=user, week=week)
    if week_stats.exists():
        day_stats = week_stats.filter(date=today)
        if day_stats.exists():
            stats = day_stats[0]
        else:
            if today.day == week.off_day:
                work_day = week.subject_week + '_off'
            else:
                week_stats = week_stats.order_by('-work_day')
                work_day = week_stats[0].work_day + 1
                program_day_string = week.subject_week + '_' + str(work_day)
            program_day = ProgramDay.objects.get(day=program_day_string)
            stats = DailyStatCollection.objects.create(
                user=user,
                week=week,
                work_day=work_day,
                program_day=program_day,
                date=today
            )
        return stats
    else:
        start_program_day_string = week.subject_week + '_0'
        start_program_day = ProgramDay.objects.get(day=start_program_day_string)
        DailyStatCollection.objects.create(
            user=user,
            week=week,
            work_day = 0,
            program_day=start_program_day,
            date=week.start_date
        )
        return getStatCollection(user)
        

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


def getSuccessCalculations(student):
    user = student.user
    start_eng = student.best_eng
    start_math = student.best_math
    start_read = student.best_read
    start_sci = student.best_sci
    hours_worked = 0
    stats = DailyStatCollection.objects.filter(user=user)
    for stat in stats:
        if stat.hours_worked:
            hours_worked += stat.hours_worked
    increase = student.goal_score - student.get_superscore()
    hours = 25 * increase
    total_points = increase * 4 + 12
    tests = TestDone.objects.filter(user=user)
    if tests.exists():
        max_eng = 0
        max_math = 0
        max_read = 0
        max_sci = 0
        for test in tests:
            if test.english_score:
                if test.english_score > max_eng:
                    max_eng = test.english_score
            if test.math_score:
                if test.math_score > max_math:
                    max_math = test.math_score
            if test.reading_score:
                if test.reading_score > max_read:
                    max_read = test.reading_score
            if test.science_score:
                if test.science_score > max_sci:
                    max_sci= test.science_score
    
        points = 0
        

        eng_points = max_eng - start_eng
        if eng_points > 0:
            points += eng_points

        math_points = max_math - start_math
        if math_points > 0:
            points += math_points

        read_points = max_read - start_read
        if read_points > 0:
            points += read_points

        sci_points = max_sci - start_sci
        if sci_points > 0:
            points += sci_points
    else:
        points = 0
    
    calculations = {
        'total_points': total_points,
        'points_increased': points,
        'total_hours': hours,
        'hours_worked': hours_worked
    }

    return calculations


def getProjections(student):
    start_eng = student.best_eng
    start_math = student.best_math
    start_read = student.best_read
    start_sci = student.best_sci

    eng_mult = .362
    math_mult = .1867
    read_mult = .25
    sci_mult = .192

    increase = student.goal_score - student.get_superscore()


    remainder = 0
    iteration = 0

    while(iteration < 2):
        eng_increase = (increase * 4 * eng_mult) + 3
        eng_increase += remainder
        eng_goal = start_eng + eng_increase
        remainder = eng_goal - 36
        if remainder > 0:
            eng_goal = 36
        else:
            remainder = 0
        eng_increase = eng_goal - start_eng

        read_increase = (increase * 4 * read_mult) + 3
        read_increase += remainder
        read_goal = start_read + read_increase
        remainder = read_goal - 36
        if remainder > 0:
            read_goal = 36
        else:
            remainder = 0
        read_increase = read_goal - start_read

        math_increase = (increase * 4 * math_mult) + 3
        math_increase += remainder
        math_goal = start_math + math_increase
        remainder = math_goal - 36
        if remainder > 0:
            math_goal = 36
        else:
            remainder = 0
        math_increase = math_goal - start_math

        sci_increase = (increase * 4 * sci_mult) + 3
        sci_increase += remainder
        sci_goal = start_sci + sci_increase
        remainder = sci_goal - 36
        if remainder > 0:
            sci_goal = 36
        else:
            remainder = 0
        sci_increase = sci_goal - start_sci

        if remainder == 0:
            break
        iteration += 1


        projections = {
        'start_score': student.get_superscore(),
        'goal_score': student.goal_score,
        'eng_goal': roundup(eng_goal),
        'math_goal': roundup(math_goal),
        'read_goal': roundup(read_goal),
        'sci_goal': roundup(sci_goal),
        }

        return projections