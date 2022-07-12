from django.urls import path
from . import views
from .subject_views import english_views, math_views, reading_views, science_views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='contact'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.logout, name='logout'),
    path('data/', views.add_data, name='add_data'),
    path('inputstats/', views.input_stats, name='input_stats'),
    path('newtest/', views.new_test, name='new_test'),
    path('newchallenge/', views.new_challenge, name='new_challenge'),
    path('newcategory/', views.new_category, name='new_category'),
    path('newlesson/', views.new_lesson, name='new_lesson')
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

urlpatterns = urlpatterns + english_urls + math_urls
