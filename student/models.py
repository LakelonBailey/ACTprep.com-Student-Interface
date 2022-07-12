from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class StudentProfile(models.Model):
    user = models.OneToOneField(
                                User,
                                on_delete=models.CASCADE,
                                null=False,
                                default=None
                                )
    student_id = models.CharField(max_length=10, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    parent_phone = models.CharField(max_length=20, null=True)
    best_comp = models.IntegerField(null=True)
    best_eng = models.IntegerField(null=True)
    best_math = models.IntegerField(null=True)
    best_read = models.IntegerField(null=True)
    best_sci = models.IntegerField(null=True)
    goal_score = models.IntegerField(null=True)
    is_leadership_team = models.BooleanField(default=False)
    event_name = models.CharField(max_length=200, null=True)

    def get_superscore(self):
        eng = self.best_eng
        math = self.best_math
        read = self.best_read
        sci = self.best_sci
        return ((eng + math + read + sci)/4)

    def get_full_name(self):
        return (self.user.first_name + ' ' + self.user.last_name)

    def __str__(self):
        return (self.user.first_name + ' ' + self.user.last_name)


class WeeklyMemorizationInfo(models.Model):
    week = models.CharField(max_length=100, null=True)
    memorization_link = models.CharField(max_length=500, null=True)
    answer_sheet = models.CharField(max_length=500, null=True)
    quizlet = models.CharField(max_length=500, null=True)
    extra_practice = models.CharField(max_length=500, null=True)
    practice_quiz_link = models.CharField(max_length=500, null=True)
    video_link = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.week


class StudentWeek(models.Model):
    user = models.ForeignKey(
                            User,
                            on_delete=models.CASCADE,
                            null=False,
                            default=None
                            )
    memorization_week = models.ForeignKey(
                                        WeeklyMemorizationInfo,
                                        on_delete=models.SET_NULL,
                                        null=True
                                        )

    start_day = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    off_day = models.IntegerField()
    test_days = ArrayField(models.IntegerField(), null=True)

    subject_week = models.CharField(max_length=200, null=True)

    def __str__(self):
        name = ''
        name += self.user.first_name + ' '
        name += self.user.last_name + ' '
        name += self.subject_week
        return name


class DailyStatCollection(models.Model):
    user = models.ForeignKey(
                            User,
                            null=False,
                            default=None,
                            on_delete=models.CASCADE
                            )
    week = models.ForeignKey(StudentWeek, on_delete=models.CASCADE, null=False, default=None)
    day = models.IntegerField(null=True)
    did_check_in = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    hours_worked = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    memorization_time = models.IntegerField(null=True)
    practice_quiz_score = models.IntegerField(null=True)

    def __str__(self):
        name = self.user.first_name + ' ' + self.user.last_name
        date = self.date.strftime("%m/%d/%y")
        return (name + ' ' + '(' + date + ')')


class Test(models.Model):
    name = models.CharField(max_length=100, null=True)
    test_location = models.CharField(max_length=500, null=True)

    english_order = models.IntegerField(null=True)
    english_location = models.CharField(max_length=500, null=True)
    english_answers = models.CharField(max_length=500, null=True)

    math_order = models.IntegerField(null=True)
    math_location = models.CharField(max_length=500, null=True)
    math_answers = models.CharField(max_length=500, null=True)

    reading_order = models.IntegerField(null=True)
    reading_location = models.CharField(max_length=500, null=True)
    reading_answers = models.CharField(max_length=500, null=True)

    science_order = models.IntegerField(null=True)
    science_location = models.CharField(max_length=500, null=True)
    science_answers = models.CharField(max_length=500, null=True)

    conversion_chart_link = models.CharField(max_length=500, null=True)
    full_test_order = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class TestDone(models.Model):
    user = models.ForeignKey(
                            User,
                            on_delete=models.SET_NULL,
                            null=True
                            )
    day = models.ForeignKey(
                            DailyStatCollection,
                            on_delete=models.SET_NULL,
                            null=True
                            )
    test = models.ForeignKey(
                            Test,
                            on_delete=models.SET_NULL,
                            null=True
                            )

    was_challenge_test = models.BooleanField()

    english_tried = models.IntegerField(null=True)
    english_correct = models.IntegerField(null=True)
    english_score = models.IntegerField(null=True)

    math_tried = models.IntegerField(null=True)
    math_correct = models.IntegerField(null=True)
    math_score = models.IntegerField(null=True)

    reading_tried = models.IntegerField(null=True)
    reading_correct = models.IntegerField(null=True)
    reading_score = models.IntegerField(null=True)

    science_tried = models.IntegerField(null=True)
    science_correct = models.IntegerField(null=True)
    science_score = models.IntegerField(null=True)

    def get_composite(self):
        comp_total = self.english_score + self.math_score + self.reading_score + self.science_score
        comp = comp_total/4
        return comp


class Challenge(models.Model):
    subject = models.CharField(max_length=100)
    order = models.IntegerField(null=True)
    test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True)
    questions_to_do = models.CharField(max_length=300)
    total_questions = models.IntegerField(null=True)
    answers_link = models.CharField(max_length=500)
    time_allowed = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.subject.capitalize() + ' ' + self.test.name + ' ' + self.questions_to_do


class ChallengeDone(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    day = models.ForeignKey(DailyStatCollection, on_delete=models.SET_NULL, null=True)
    challenge = models.ForeignKey(Challenge, on_delete=models.SET_NULL, null=True)
    total_correct = models.IntegerField(null=True)


class CategoryGroup(models.Model):
    subject = models.CharField(max_length=100, null=False, default='english')
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    group = models.ForeignKey(CategoryGroup, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return 'Name: ' + self.name + ' - Group: ' + self.group.name


class CategoryDone(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    day = models.ForeignKey(DailyStatCollection, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    time_spent = models.IntegerField(null=True)


class Lesson(models.Model):
    subject = models.CharField(max_length=100, null=False, default='english')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=300)
    can_embed = models.BooleanField(default=False)
    link = models.CharField(max_length=500)
    time = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class LessonDone(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    day = models.ForeignKey(DailyStatCollection, on_delete=models.SET_NULL, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    time_spent = models.IntegerField(null=True)
