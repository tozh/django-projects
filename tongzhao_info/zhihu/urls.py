from django.urls import path
from . import views

urlpatterns = [
    path('person', views.person, name='zhihu-person'),
    path('simple_person', views.simple_person, name='zhihu-simple_person'),
    path('entity', views.entity, name='zhihu-entity'),
    path('top_person_of_entity', views.top_person_of_entity, name='zhihu-top_person_of_entity'),
    path('top_entity_by_person_number', views.top_entity_by_person_number, name='zhihu-top_entity_by_person_number'),
    path('top_person_by_value', views.top_person_by_value, name='zhihu-top_person_by_value'),
    path('statistic', views.statistic, name='zhihu-statistic'),
]