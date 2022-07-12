from django import forms
from .models import Category, Test, Challenge, Lesson


def get_tests():
    tests = Test.objects.all()
    tests = tests.order_by('name')
    return tests


def get_challenges():
    challenges = Challenge.objects.all()
    challenges = challenges.order_by('subject', 'order')
    return challenges


def get_categories():
    categories = Category.objects.all()
    categories = categories.order_by('group', 'name')
    return categories


def get_lessons():
    lessons = Lesson.objects.all()
    lessons = lessons.order_by('subject')
    return lessons


class DailyStatForm(forms.Form):
    hours_worked = forms.DecimalField(max_digits=4, decimal_places=2)
    memorization_time = forms.IntegerField()
    practice_quiz_score = forms.IntegerField(required=False)


class TestForm(forms.Form):
    test = forms.ModelChoiceField(queryset=get_tests(), empty_label='Select')
    english_tried = forms.IntegerField(required=False, max_value=75)
    english_correct = forms.IntegerField(required=False, max_value=75)
    english_score = forms.IntegerField(required=False, max_value=36)

    math_tried = forms.IntegerField(required=False, max_value=60)
    math_correct = forms.IntegerField(required=False, max_value=60)
    math_score = forms.IntegerField(required=False, max_value=36)


    reading_tried = forms.IntegerField(required=False, max_value=40)
    reading_correct = forms.IntegerField(required=False, max_value=40)
    reading_score = forms.IntegerField(required=False, max_value=36)

    science_tried = forms.IntegerField(required=False, max_value=40)
    science_correct = forms.IntegerField(required=False, max_value=40)
    science_score = forms.IntegerField(required=False, max_value=36)


class ChallengeForm(forms.Form):
    challenge = forms.ModelChoiceField(queryset=get_challenges(), empty_label='Select')
    total_correct = forms.IntegerField()


class CategoryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=get_categories(), empty_label='Select')
    time_spent = forms.IntegerField()


class LessonForm(forms.Form):
    lesson = forms.ModelChoiceField(queryset=get_lessons(), empty_label='Select')
    time_spent = forms.IntegerField()