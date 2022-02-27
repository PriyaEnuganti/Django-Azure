from django.urls import path

from . import views

urlpatterns = [
    path('', views.Classifier, name='Classifier'),
    path('', views.index, name='index'),
]
