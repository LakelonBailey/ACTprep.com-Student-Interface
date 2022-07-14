# Generated by Django 4.0.4 on 2022-07-14 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=100, null=True)),
                ('memorization_link', models.CharField(max_length=500, null=True)),
                ('answer_sheet', models.CharField(max_length=500, null=True)),
                ('quizlet', models.CharField(max_length=500, null=True)),
                ('extra_practice', models.CharField(max_length=500, null=True)),
                ('practice_quiz_link', models.CharField(max_length=500, null=True)),
                ('video_link', models.CharField(max_length=500, null=True)),
                ('in_class_quiz', models.CharField(max_length=500, null=True)),
                ('schedule', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
