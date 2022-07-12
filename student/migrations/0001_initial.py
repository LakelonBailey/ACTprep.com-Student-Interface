# Generated by Django 4.0.4 on 2022-07-09 19:50

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(default='english', max_length=100)),
                ('name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('order', models.IntegerField(null=True)),
                ('questions_to_do', models.CharField(max_length=300)),
                ('total_questions', models.IntegerField(null=True)),
                ('answers_link', models.CharField(max_length=500)),
                ('time_allowed', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='DailyStatCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(null=True)),
                ('did_check_in', models.BooleanField(default=False)),
                ('date', models.DateField(auto_now_add=True)),
                ('hours_worked', models.DecimalField(decimal_places=2, max_digits=4)),
                ('memorization_time', models.IntegerField(null=True)),
                ('practice_quiz_score', models.IntegerField(null=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(default='english', max_length=100)),
                ('name', models.CharField(max_length=300)),
                ('can_embed', models.BooleanField(default=False)),
                ('link', models.CharField(max_length=500)),
                ('time', models.CharField(max_length=100, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.category')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('test_location', models.CharField(max_length=500, null=True)),
                ('english_order', models.IntegerField(null=True)),
                ('english_location', models.CharField(max_length=500, null=True)),
                ('english_answers', models.CharField(max_length=500, null=True)),
                ('math_order', models.IntegerField(null=True)),
                ('math_location', models.CharField(max_length=500, null=True)),
                ('math_answers', models.CharField(max_length=500, null=True)),
                ('reading_order', models.IntegerField(null=True)),
                ('reading_location', models.CharField(max_length=500, null=True)),
                ('reading_answers', models.CharField(max_length=500, null=True)),
                ('science_order', models.IntegerField(null=True)),
                ('science_location', models.CharField(max_length=500, null=True)),
                ('science_answers', models.CharField(max_length=500, null=True)),
                ('conversion_chart_link', models.CharField(max_length=500, null=True)),
                ('full_test_order', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyMemorizationInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.CharField(max_length=100, null=True)),
                ('memorization_link', models.CharField(max_length=500, null=True)),
                ('answer_sheet', models.CharField(max_length=500, null=True)),
                ('quizlet', models.CharField(max_length=500, null=True)),
                ('extra_practice', models.CharField(max_length=500, null=True)),
                ('practice_quiz_link', models.CharField(max_length=500, null=True)),
                ('video_link', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestDone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('was_challenge_test', models.BooleanField()),
                ('english_tried', models.IntegerField(null=True)),
                ('english_correct', models.IntegerField(null=True)),
                ('english_score', models.IntegerField(null=True)),
                ('math_tried', models.IntegerField(null=True)),
                ('math_correct', models.IntegerField(null=True)),
                ('math_score', models.IntegerField(null=True)),
                ('reading_tried', models.IntegerField(null=True)),
                ('reading_correct', models.IntegerField(null=True)),
                ('reading_score', models.IntegerField(null=True)),
                ('science_tried', models.IntegerField(null=True)),
                ('science_correct', models.IntegerField(null=True)),
                ('science_score', models.IntegerField(null=True)),
                ('day', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.dailystatcollection')),
                ('test', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.test')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentWeek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_day', models.IntegerField()),
                ('start_date', models.DateField()),
                ('off_day', models.IntegerField()),
                ('test_days', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None)),
                ('subject_week', models.CharField(max_length=200, null=True)),
                ('memorization_week', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.weeklymemorizationinfo')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=10, null=True)),
                ('first_name', models.CharField(max_length=200, null=True)),
                ('last_name', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('parent_phone', models.CharField(max_length=20, null=True)),
                ('best_comp', models.IntegerField(null=True)),
                ('best_eng', models.IntegerField(null=True)),
                ('best_math', models.IntegerField(null=True)),
                ('best_read', models.IntegerField(null=True)),
                ('best_sci', models.IntegerField(null=True)),
                ('goal_score', models.IntegerField(null=True)),
                ('is_leadership_team', models.BooleanField(default=False)),
                ('event_name', models.CharField(max_length=200, null=True)),
                ('user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LessonDone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_spent', models.IntegerField(null=True)),
                ('day', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.dailystatcollection')),
                ('lesson', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.lesson')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='dailystatcollection',
            name='week',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='student.studentweek'),
        ),
        migrations.CreateModel(
            name='ChallengeDone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_correct', models.IntegerField(null=True)),
                ('challenge', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.challenge')),
                ('day', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.dailystatcollection')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='challenge',
            name='test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.test'),
        ),
        migrations.CreateModel(
            name='CategoryDone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_spent', models.IntegerField(null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.category')),
                ('day', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.dailystatcollection')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.categorygroup'),
        ),
    ]
