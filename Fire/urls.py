from django.urls import path

from . import views

urlpatterns = [
    path('', views.FireClassifier, name='FireClassifier'),
    path('', views.index, name='index'),
]
