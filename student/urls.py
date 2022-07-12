from django.urls import path
from . import views, api_views
from .subject_views import english_views, math_views, reading_views, science_views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='contact'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.logout, name='logout')
]

english_urls = [
    path('english/', english_views.index, name='english'),
]

math_urls = [
    path('math/', math_views.index, name='math'),
]

reading_urls = [
    path('reading/', reading_views.index, name='math'),
]

science_urls = [
    path('science/', science_views.index, name='math'),
]

api_urls = [
    path('checkin/', api_views.check_in, name='check_in'),
    path('data/', api_views.add_csv_data, name='add_csv_data'),
    path('inputstats/', api_views.input_stats, name='input_stats'),
    path('newtest/', api_views.new_test, name='new_test'),
    path('newchallenge/', api_views.new_challenge, name='new_challenge'),
    path('newcategory/', api_views.new_category, name='new_category'),
    path('newlesson/', api_views.new_lesson, name='new_lesson')
]

urlpatterns = urlpatterns + english_urls + math_urls + api_urls
