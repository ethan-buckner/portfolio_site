from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('input_combo', views.input_combo, name='input_combo'),
    path('result', views.result, name='result')
]